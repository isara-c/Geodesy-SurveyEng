# CR : 31(B) Mr.Isara Chaowuttisuk
# Problem CW 5-9 Vertex of Geodesic
print('******** Problem CW 5-9 by CR:31(B) Mr.Isara Chaowuttisuk ********' +'\n')

from math import radians, degrees, sin, cos, pi, sqrt, acos
# นำเข้าโมดูล math เพื่อใช้ฟังก์ชันตรีโกณ

def radius_N( phi ) : # คำนวณ N ของแบบจำลอง WGS84
    N = a /  sqrt( 1- ( e_2 * sin( phi )**2 ) )
    return N

def vertex_iteration( phi, Az  ) : # ฟังก์ชัน คำนวณ vertex ด้วยวิธีวนลูป
    phi, Az =  radians( phi ), radians( Az ) # แปลง phi และ Az เป็น radians
    cc = radius_N( phi ) * cos ( phi ) * sin ( Az ) # คำนวณหา clairaut const.
    phi_max_i = acos( cc / radius_N( phi ) ) # คำนวณหา Phi max จากสูตร
    diff, loop_i =  1, 0 # ตั้งค่าเริ่มต้นของผลต่างเพื่อเริ่ม loop
    print('------------------- iteration find phi_max ---------------------')
    while diff != 0: # วนลุปจนกระทั่งผลต่างมีค่าเป็นศุนย์
        phi_max = acos( cc / radius_N( phi_max_i ) )
        diff, phi_max_i = abs(phi_max - phi_max_i), phi_max  # นำค่า phi_max จากครั้งก่อนมาแทนค่า
        print( 'iter:{}   diff: {}   phi_max: {} deg.'.format\
        ( loop_i, str( diff ).ljust( 23 ), str( 180-degrees( phi_max )).ljust( 18 ) ))
        loop_i += 1
    print('----------------------------- end ------------------------------', '\n')
    return degrees( phi_max )

def vertex_Phisan( phi, Az ) : #  ฟังก์ชั่นคำนวณ vertex ด้วยวิธีวิเคราะห์สูตร ของอาจารย์ไพศาล
    phi, Az =  radians( phi ), radians( Az )
    cc = radius_N( phi ) * cos ( phi ) * sin ( Az )
    phi_max = acos( sqrt( ( cc**2*( 1 - e_2 ) )  / ( a**2 - cc**2 * e_2 )  ))
    return degrees( phi_max ) 

a, f  = 6378137, 1/298.257223563
e_2 = 1 - ( 1-f )**2

lat1,  Az1 = 26.27083, 139.79969 # พิกัด latitude และ forward Az
vertex_iter, vertex_Phisan = vertex_iteration( lat1, Az1 ) ,vertex_Phisan( lat1, Az1 )

print( 'Phi_max by iteration :      ', vertex_iter )
print( 'Phi_max by P.santitamnont : ', vertex_Phisan )