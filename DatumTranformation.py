# Problem CW 5-10 RID Datum Transformation(Shift parameter)
# CR 31 Mr.Isara  Chaowuttisuk
print('Problem CW 5-10 RID Datum Transformation(Shift parameter) by CR 31 Mr.Isara Chaowuttisuk' + '\n')

from math import sin, cos, atan2, sqrt, radians, degrees, pow 
import numpy as np

IND75  = { 'a' : 6377276.345 ,  'rf' : 300.8017 }       # ค่าใน Datum INDIAN1975
WGS84  = { 'a' : 6378137.0   ,  'rf' : 298.257223563 }  # ค่าใน Datum WGS84

def Radius_MN( datum, Lat): # ฟังก์ชันคำนวณ M และ N เนื่องจากเป็นทรงรี
    a, e2 = datum[ 'a' ] , 1 /  datum[ 'rf' ] * (2-1/datum[ 'rf' ] )
    M = a * ( 1-e2 ) /  sqrt( 1- ( e2 * sin( Lat )**2 ) )   # คำนวณค่า M
    N = a /  sqrt( 1- ( e2 * sin( Lat )**2 ) )              # คำนวณค่า N
    return ( M,N )

def Radius_MNcosP( datum, Lat): # ฟังก์ชันคำนวณหา NcosP เพื่อหาผลต่าง N, E, U
    M, a = Radius_MN( datum, Lat)[ 0 ], datum[ 'a' ]
    NcosP = a * cos( radians( Lat ) )    
    return ( M, NcosP )

def PLh2XYZ( datum , Phi_Lam_h ): # ฟังก์ชันแปลงค่าพิกัด phi, lamda, height เป็น X, Y, Z
    P, L, h  = Phi_Lam_h # กำหนดตัวแปร P, L, h เก็บค่า phi, lamda, height
    P, L     = radians( P ), radians( L ) # แปลงเป็นเรเดียน
    N, e2    = Radius_MN( datum, P )[ 1 ], 1 / datum[ 'rf' ]*( 2-1/datum[ 'rf' ] )
    # คำนวณหา N จากฟังก์ชัน Radius_MN และหาค่า e กำลังสอง
    X        = ( N + h ) * cos(P) * cos(L)  # คำนวนค่าพิกัด X ในระบบ ECEF
    Y        = ( N + h ) * cos(P) * sin(L)  # คำนวนค่าพิกัด Y ในระบบ ECEF
    Z        = ( ( 1 - e2 ) * N +  h) * sin(P)  # คำนวนค่าพิกัด Z ในระบบ ECEF
    return ( X, Y, Z )

def XYZ2PLh( datum, XYZ): # ฟังก์ชันแปลงค่าพิกัด X, Y, Z  เป็น phi, lamda, height โดยใช้อัลกอริทึมของ Vermeille 2011
    X, Y, Z   = XYZ # กำหนดตัวแปร X, Y, Z เก็บค่าพิกัดในระบบ ECEF
    a2, e2    = datum[ 'a' ]**2 , 1 / datum['rf'] * ( 2 - 1 / datum[ 'rf' ] )
    sqrt_X2Y2, e4   = sqrt( X**2 + Y**2 ), e2 * e2
    p = ( X**2 + Y**2 ) / ( a2 ) 
    q = (1. - e2 ) * Z**2 / a2
    r = ( p + q - e2**2 ) / 6.
    e4pq = e4 * p * q 
    evol = 8 * pow( r, 3 ) + e4pq
    if evol > 0.:
        sqrt_8r3_e4qp = sqrt( evol )
        sqrt_e4pq     = sqrt( e4pq )
        try: u = r + 0.5 * pow( sqrt_8r3_e4qp + sqrt_e4pq , 2/3.) + 0.5 * pow( sqrt_8r3_e4qp - sqrt_e4pq , 2/3.)
        except ValueError:
            print('*** XYZ2PLh_Vermeille2004() : the point is near or inside the evolute ***')
            print('sqrt_8r3_e4qp={} sqrt_e4pq={}'.format(sqrt_8r3_e4qp, sqrt_e4pq)  )
            print('*** not yet handled. ***')
            exit(-1)
    else:  # evil <=0
        print('*** XYZ2PLh_Vermeille2004() : the point is near or inside the evolute ***')
        print('*** evol <= 0 *** not yet handled. ***')
        exit(-1)        

    v = sqrt( u*u + e4*q )
    w = e2 * ( u+v-q) / (2*v)
    k = ( u+v ) / ( sqrt( w* w+u+v) + w   )
    D = k * sqrt_X2Y2 / ( k+e2 )
    sqrt_D2Z2 = sqrt( D*D + Z**2)
    
    hae = ( k + e2-1.) * sqrt_D2Z2 / k # คำนวณความสูง(height) ตามสูตร
    Phi = degrees( 2 * atan2( Z, sqrt_D2Z2 + D ) )# คำนวณละติจูด ตามสูตร
    Lam = degrees( 2 * atan2( Y, sqrt_X2Y2 + X ) )# คำนวณลองจิจูด ตามสูตร
    return  ( Phi, Lam, hae )

############################################################
P1 = ( 15.09598994, 100.28250582, -6.151 ) ; P1_fixed = (15.09754023, 100.27924296, -16.853 ) # พิกัดหมุดที่1(IND75) และพิกัดกรมชล(WGS84)
P2 = ( 15.09402501, 100.28262742, -6.085  ); P2_fixed = (15.09557546, 100.27936458, -16.793 ) # พิกัดหมุดที่2(IND75) และพิกัดกรมชล(WGS84)

for [ P, P_fixed ] in [ (P1, P1_fixed ), (P2, P2_fixed ) ]: # ลูปวนอ่านค่าพิกัด(IND75) และพิกัดกรมชล(WGS84) สำหรับการวนหนึ่งครั้ง
    print( '------------------------  start New Point  ----------------------------'   )
    Point_IND75_PLh = ( P )  # P( lat, lon, h ) ทำการกำหนดค่าพิกัด datum IND75 (PLh)  เก็บไว้ในตัวแปร 
    Point_IND75_XYZ  = PLh2XYZ(  IND75, Point_IND75_PLh ) # ทำการแปลงค่าพิกัด( Datum Indain 1975 ) มาเป็นระบบ ECEF ( X, Y, Z )
    print( 'Point(IND75) in XYZ', '\n', '   X = {:.3f} m.    Y = {:.3f} m.      Z = {:.3f} m. '.format( *Point_IND75_XYZ )  + '\n'  )

    TO_WGS84 = [ 204.4798, 837.8940,  294.7765 ] # กำหนด shift parameter สำหรับการแปลง datum indian1975 มาเป็น datum WGS84             
    Point_WGS84_XYZ = np.array( Point_IND75_XYZ )  + np.array( TO_WGS84 )  # ทำการแปลง datum indian1975 มาเป็น datum WGS84 
    print( 'Point(WGS84) in XYZ', '\n',  '   X = {:.3f} m.    Y = {:.3f} m.      Z = {:.3f} m. '.format( *Point_WGS84_XYZ )  + '\n'  )

    Point_WGS84_PLh = XYZ2PLh(  WGS84,  Point_WGS84_XYZ ) # ทำการแปลงพิกัด(Datum_WGS84) จากระบบ ECEF( X, Y, Z) มาเป็นระบบ PLh
    print( 'Point(WGS84) in PLh', '\n', '   lat = {:.5f} deg.  lng = {:.5f} deg.  h = {:.3f} m.    '.format( *Point_WGS84_PLh ) + '\n'    )

    print('------------------------  diffference N, E, U ----------------------'  )  # หาผลต่างของค่าที่คำนวณด้วย python เทียบกับพิกัดกรมชล
    Point_WGS84_Fixed = ( P_fixed ) # กำหนดพิกัดกรมชล(datum WGS84) เก็บไว้ในตัวแปร
    DIFF = np.array( Point_WGS84_Fixed ) - np.array( Point_WGS84_PLh) # หาผลต่างระหว่างพิกัดจากกรมชล และพิกัดที่คำนวณด้วย python
    print( 'Difference: Diff_lat = {:.6f} sec.  Diff_lng = {:.6f} sec.     Diff_h = {:.4f}    m.    '.format( 
        abs(3600*DIFF[0]), abs(3600*DIFF[1]), abs(DIFF[2])  ) + '\n'   )
    M,NcosP = Radius_MNcosP( WGS84 , Point_WGS84_PLh[0] ) # หาค่า M และ NcosP เพื่อนำมาหาผลค่าผลต่าง E, N, U
    print( 'Difference: Diff_N   = {:.3f} m.      Diff_E = {:.3f} m.           Diff_U = {:.3f}    m.    '.format( 
        M * radians( abs(DIFF[0]) ),  NcosP * radians( abs(DIFF[1]) ), abs(DIFF[2])     )  +'\n'    )
    print('************************ End of Datum Transformation for this point***********************' + '\n' + '\n' + '\n' )