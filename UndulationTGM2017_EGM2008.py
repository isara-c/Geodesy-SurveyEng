# Problem : Undulation EGM2008 and TGM2017

import subprocess

GEIOEVAL_TGM2017 =  'geoideval -n tgm2017-1 --input-string "{} {}"'
# กำหนดคำสั่ง command ที่ต้องการเรียกใช้(หา N จากแบบจำลอง TGM2017) ให้อยู่ในรูปแบบ string
# โดยกำหนดตัวแปรสตริง(format) ให้สามารถแทนค่าได้ 2 ตัว (lat, lng)
GEIOEVAL_EGM2008 =  'geoideval -n egm2008-1 --input-string "{} {}"'
# กำหนดคำสั่ง command ที่ต้องการเรียกใช้(หา N จากแบบจำลอง EGM2008) ให้อยู่ในรูปแบบ string
# โดยกำหนดตัวแปรสตริง(format) ให้สามารถแทนค่าได้ 2 ตัว (lat, lng)


def GeoidUndul_TGM2017( lat, lng): # ฟังก์ชันในการหาค่า N โดยเรียกใช้ command ด้วย subprocess 
    cmd = GEIOEVAL_TGM2017.format( lat, lng )# แทนค่า parameter(lat,lng) ลงในคำสั่ง commmand 
    result = subprocess.run( cmd,  shell=True, check=True , capture_output=True )
    # run command แล้วเรียกใช้คำสั่งที่กำหนดไว้ในตัวแปร CMD และเก็บผลลัพธ์ไว้ใน Result
    undul = float( result.stdout)# ตัดตัวอักษรที่ไม่เกี่ยวข้องออกด้วย .stdout และแปลงเป็น float 
    return undul # คืนค่า Geoid Undulation ; N (meter)

def GeoidUndul_EGM2008( lat, lng):
    cmd = GEIOEVAL_EGM2008.format( lat, lng )# แทนค่า parameter(lat,lng) ลงในคำสั่ง commmand 
    result = subprocess.run( cmd,  shell=True, check=True , capture_output=True )
    # run command แล้วเรียกใช้คำสั่งที่กำหนดไว้ในตัวแปร CMD และเก็บผลลัพธ์ไว้ใน Result
    undul = float( result.stdout)# ตัดตัวอักษรที่ไม่เกี่ยวข้องออกด้วย .stdout และแปลงเป็น float 
    return undul # คืนค่า Geoid Undulation ; N (meter)

lat, lng = 14, 100 # กำหนดค่า latitude และ logitude ให้เท่ากับ 14 และ 100
N_EGM2008 =  GeoidUndul_EGM2008( lat, lng) # หาค่า N จากแบบจำลอง EGM2008
N_TGM2017 =  GeoidUndul_TGM2017( lat, lng) # หาค่า N จากแบบจำลอง TGM2017

print( 'EGM2008  |  TGM2017 |  Diff')
print( N_EGM2008, ' ' , N_TGM2017 ,' ', '{:.4f}'.format( abs(N_EGM2008 - N_TGM2017) ) )
