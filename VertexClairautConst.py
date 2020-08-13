# Problem : Vertex / Clairaut Conts

from math import radians, degrees, sin, cos, pi, sqrt, acos, asin # นำเข้า module math เพื่อใช้ตรีโกณ
from geographiclib.geodesic import Geodesic # นำเข้าเพื่อใช้หาค่าพิกัดทางภูมิศาสตร์
import numpy as np
import matplotlib.pyplot as plt # นำเข้าเพื่อพลอตกราฟละติจูดและลองจิจูด

geod = Geodesic.WGS84 # ใส่ประเภทของ Datum ทีใช้คือ WGS84  
a, f  = geod.a , geod.f # เรียกใช้ค่า a, f จากโมดูล geographiclib.geodesic
e_2 = 1 - ( 1-f )**2 # คำนวณค่า e กำลังสอง

lat = { 'AMS_A': 52.308613, 'BAH_B' : 26.270833 }
lng = { 'AMS_A': 4.763889,  'BAH_B' : 50.633611 }

def radius_N( phi ) : # ฟังก์ชันคำนวณหาค่า N จากแบบจำลอง WGS84
    N = a /  sqrt( 1- ( e_2 * sin( phi )**2 ) )
    return N

def InverseProblem ( lat1, lng1, lat2, lng2 ):
    #เรียกใช้ module ในการแก้ปัญหา InverseProblem 
    g = geod.Inverse( lat1, lng1, lat2, lng2)
    Az1, Az2, s12 = g[ 'azi1' ], g[ 'azi2' ], g[ 's12' ]
    return ( Az1, Az2, s12 )

def DirectProblem ( lat1, lng1, Az1, s12 ):
    #เรียกใช้ module ในการแก้ปัญหา DirectProblem 
    g = geod.Direct( lat1, lng1, Az1, s12 )
    lat2, lng2, Az2 = g[ 'lat2' ], g[ 'lon2' ], g[ 'azi2' ]
    return ( lat2, lng2, Az2 )

def vertex_Phisan( phi, Az ) : #ฟังก์ชันคำนวณ vertex ใช้สูตรวิเคราะห์จากอาจารย์ไพศาล
    phi, Az =  radians( phi ), radians( Az )
    cc = radius_N( phi ) * cos ( phi ) * sin ( Az )
    phi_max = acos( sqrt( ( cc**2*( 1 - e_2 ) )  / ( a**2 - cc**2 * e_2 )  ))
    return ( degrees( phi_max ), cc ) 

################# แบ่งระยะทาง s12 เป็น 10 ช่วง #####################
geod_line = geod.InverseLine( lat['BAH_B'], lng['BAH_B'] , lat['AMS_A'], lng['AMS_A'] )
SEGMENTS = np.linspace( 0, geod_line.s13, num=11, endpoint=True ) # แบ่งระยะออกเป็น 10 ช่วง จะได้ทั้งหมด 11 จุด

####################### Plot route  & Find clairaut const. ########################
print( '\n'+'------------  Find dist, lat, lng, Az of 10 points  -------------')
print( "| =distance= | =latitude= |  =azimuth= |  clairaut const. " )

lats = [] ; lngs = [] ; az2s = [] # สร้างลิสท์ไว้เก็บข้อมูล
for seg in SEGMENTS:# หาค่าละติจูด ลองจิจูดเพื่อนำไปพลอตกราฟ
    pos = geod_line.Position( seg, Geodesic.STANDARD | Geodesic.LONG_UNROLL ) # ไม่ให้ค่าติดลบ จะได้ค่าเป็น 0ถึง360
    lats.append( pos['lat2'] ) # เพิ่มค่าละติจูดลงในลิสท์ lats
    lngs.append( pos['lon2'] ) # เพิ่มค่าลองจิจูดลงในลิสท์ lngs
    az2s.append( '{:.1f}'.format( pos['azi2'] ) ) # เพิ่มค่า Azimuth แต่ละจุดลงในลิสท์
    # เพิ่มค่าละติจูดลงในลิสท์ lats และ เพิ่มค่าลองจิจูดลงในลิสท์ lngsและเพิ่มค่า Azimuth แต่ละจุดลงในลิสท์
    vertex, cc =  vertex_Phisan( pos['lat2'], pos['azi2'] )
    print( "| {:10.0f} | {:10.5f} | {:10.5f} | {:.8f} m. ".format(pos['s12'], pos['lat2'], pos['azi2']+180, abs(cc) ) )

    ######################### Extent line with DirectProblem ########################
print( '\n'+'------------  Extent line with Direct Problem  -------------')
print( "| =distance= | =latitude= |  =azimuth= |  clairaut const. " )
s = float( geod_line.s13/10) ; 
for i in range(10):# หาค่าละติจูด ลองจิจูดเพื่อนำไปพลอตกราฟ
    lat2, lng2, az2 = DirectProblem ( float(lats[-1]), float(lngs[-1]), float(az2s[-1]), s )
    lats.append( lat2 ) # เพิ่มค่าละติจูดลงในลิสท์ lats
    lngs.append( lng2 ) # เพิ่มค่าลองจิจูดลงในลิสท์ lngs
    az2s.append( '{:.1f}'.format( az2 ) ) # เพิ่มค่า Azimuth แต่ละจุดลงในลิสท์
    # เพิ่มค่าละติจูดลงในลิสท์ lats และ เพิ่มค่าลองจิจูดลงในลิสท์ lngs และ เพิ่มค่า Azimuth แต่ละจุดลงในลิสท์
    vertex, cc =  vertex_Phisan( pos['lat2'], pos['azi2'] )
    print( "| {:10.0f} | {:10.5f} | {:10.5f} | {:.8f} m. ".format( s*(i+1), lat2, az2+180, abs(cc) ) )

###################### Find vertex and geodesic ###################### 
print( '\n'+"vertex phi max : {:.6f} deg. ".format( vertex ) + '\n' )


######################### plot graph #############################
plt.title('Route from AMS to BAH ')
plt.plot( lngs, lats, linewidth=2 ,color = 'r' ) # ตั้งค่าความหนาเส้น กับสี
plt.grid( axis='both' ) # พลอตเส้นกริด
plt.xlabel('longitude') # ตั้งชื่อแกน X
plt.ylabel('latitude') # ตั้งชื่อแกน Y
plt.show() # แสดงกราฟที่ได้
