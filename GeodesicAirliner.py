# Problem : Inverse Geodesic using GeographicLib

from geographiclib.geodesic import Geodesic
geod = Geodesic.WGS84 # กำหนดให้เป็นแบบจำลอง WGS84


def Geodesic_Inverse( lat1, lng1, lat2, lng2 ):  # สร้างฟังก์ชันเพื่อหา Geodesic ด้วยวิธิ Inverse
    result = geod.Inverse(lat1, lng1, lat2, lng2)
    # กำหนด result เพื่อรองรับผลลัพธ์จากการเรียกใช้ Geodesic
    fwd_Az1, fwd_Az2, s12 = result['azi1'], result['azi2'], result['s12']
    # กำหนด forward แอซิมัธของจุดต้นทางและเก็บค่าแอซิมัธ
    return fwd_Az1, fwd_Az2, s12 

fwd_Az1, fwd_Az2, s12 = Geodesic_Inverse( 52.30861, 4.76389, 26.27083, 50.6336 )
# เก็บค่าที่ออกมาจากการใช้ฟังก์ชันไว้ในตัวแปรทั้งสามตัว

print('      fwd_Az1     |      fwd_Az2      |      Distance')
print( '   {:.5f}        {:.5f}        {:.3f} m. '.format(fwd_Az1, fwd_Az2, s12))
