# Problem Undulation EGM2008 and TGM2017

import numpy as np
import subprocess 
import matplotlib.pyplot as plt

GEIOEVAL_TGM2017 = r'geoideval -n tgm2017-1 --input-string "{} {}"'
GEIOEVAL_EGM2008 = r'geoideval -n egm2008-1 --input-string "{} {}"'
# กำหนดคำสั่ง command ที่ต้องการเรียกใช้(หา N จากแบบจำลอง TGM2017) ให้อยู่ในรูปแบบ string
# โดยกำหนดตัวแปรสตริง(format) ให้สามารถแทนค่าได้ 2 ตัว (lat, lng)

def GeoidUndul_TGM( lat, lng):# ฟังก์ชันในการหาค่า N โดยเรียกใช้ command ด้วย subprocess 
    CMD = GEIOEVAL_TGM2017.format( lat, lng )# แทนค่า parameter(lat,lng) ลงในคำสั่ง commmand
    Result = subprocess.run( CMD,  shell=True, check=True , capture_output=True )
    # run command แล้วเรียกใช้คำสั่งที่กำหนดไว้ในตัวแปร CMD และเก็บผลลัพธ์ไว้ใน Result
    undul = float( Result.stdout) # ตัดตัวอักษรที่ไม่เกี่ยวข้องออกด้วย .stdout และแปลงเป็น float 
    return undul # คืนค่า Geoid Undulation ; N (meter)

def GeoidUndul_EGM( lat, lng):# ฟังก์ชันในการหาค่า N โดยเรียกใช้ command ด้วย subprocess 
    CMD = GEIOEVAL_EGM2008.format( lat, lng )# แทนค่า parameter(lat,lng) ลงในคำสั่ง commmand
    Result = subprocess.run( CMD,  shell=True, check=True , capture_output=True )
    # run command แล้วเรียกใช้คำสั่งที่กำหนดไว้ในตัวแปร CMD และเก็บผลลัพธ์ไว้ใน Result
    undul = float( Result.stdout) # ตัดตัวอักษรที่ไม่เกี่ยวข้องออกด้วย .stdout และแปลงเป็น float 
    return undul # คืนค่า Geoid Undulation ; N (meter)

n = 10 # กำหนดจำนวนจุดของละติจูดและลองจิจูดที่ต้องการ
LATS = np.linspace( 17.7, 18.7, n, endpoint=True) # แบ่งช่วงละติจูดออกเป็นจุดตามจำนวนที่ต้องการ
LNGS = np.linspace( 99.5, 100.5,  n, endpoint=True)  # แบ่งช่วงลองจิจูดออกเป็นจุดตามจำนวนที่ต้องการ
x, y = np.meshgrid( LNGS, LATS ) # สร้าง x,y ให้เป็น array 2 มิติ ที่เก็บค่าละติจูดและลองจิจูดตามลำดับ

UNDUL_TGM, z1  = [], np.zeros( [ n, n ] ) # สร้าง z ให้เป็น array 2 มิติ เพื่อรองรับค่า Undulation
UNDUL_EGM, z2  = [], np.zeros( [ n, n ] )

fig = plt.figure() # สร้างรูปภาพเพื่อรองรับกราฟทั้งสองกราฟ

plt1 = fig.add_subplot(221) # สร้างกราฟย่อย จากคำสั่ง add_subplot(nrows, ncols, plot_number)
plt1.set_title( 'N_TGM : Phare' ) # กำหนดชื่อกราฟย่อย1 
plt1.grid( axis = 'both' ) # สร้าง grid ของแกน x และ y

plt2 = fig.add_subplot(222) # สร้างกราฟย่อยเพื่อแสดง iso-line
plt2.set_title( ' Contour_TGM : Phare' ) # กำหนดชื่อกราฟย่อย2
plt2.grid( axis = 'both' ) # สร้าง grid ของแกน x และ y

plt3 = fig.add_subplot(223) # สร้างกราฟย่อย จากคำสั่ง add_subplot(nrows, ncols, plot_number)
plt3.set_title( 'N_EGM : Phare' ) # กำหนดชื่อกราฟย่อย1 
plt3.grid( axis = 'both' ) # สร้าง grid ของแกน x และ y

plt4 = fig.add_subplot(224) # สร้างกราฟย่อย จากคำสั่ง add_subplot(nrows, ncols, plot_number)
plt4.set_title( 'Contour_EGM : Phare' ) # กำหนดชื่อกราฟย่อย1 
plt4.grid( axis = 'both' ) # สร้าง grid ของแกน x และ y

for i,lat in enumerate( LATS ): # ใช้คำสั่ง enumerate เพื่อหา index และ value

    for j,lng in enumerate( LNGS) : # เรียกใช้ค่า lat, lng ใน list ที่เก็บค่าจุดพิกัด lat,lng
        undul1, undul2 = GeoidUndul_TGM( lat, lng), GeoidUndul_EGM( lat, lng)
        # เรียกใช้ฟังก์ชัน GeoidUndul เพื่อหา Undulation
        UNDUL_TGM.append( undul1 ) # เพิ่มค่า undulation ลงไปใน list ที่เก็บค่า Undulation
        UNDUL_EGM.append( undul2 ) # เพิ่มค่า undulation ลงไปใน list ที่เก็บค่า Undulation
        z1[i,j], z2[i,j] = undul1, undul2 # ใส่ค่า Undulation ลงใน array z
        plt1.scatter( lng, lat ) # ทำการ plot จุดที่แสดงค่า undulation
        plt1.text(lng, lat, '{:.2f}'.format( undul1 ) , fontsize = 8, rotation=45 ) # เขียนค่า N กำกับแต่ละจุด
        plt3.scatter( lng, lat ) # ทำการ plot จุดที่แสดงค่า undulation
        plt3.text(lng, lat, '{:.2f}'.format( undul2 ), fontsize = 8 , rotation=45 ) # เขียนค่า N กำกับแต่ละจุด

levels1 = np.arange( min( UNDUL_TGM ) // 1 , max( UNDUL_TGM ), 0.5 ) # กำหนดระยะห่างชั้น contour เท่ากับ 0.5
levels2 = np.arange( min( UNDUL_EGM ) // 1 , max( UNDUL_EGM ), 0.5 ) # กำหนดระยะห่างชั้น contour เท่ากับ 0.5

ct_TGM = plt2.contour( x, y, z1, levels1 ) # plot กราฟ contour ลงในกราฟย่อยที่ 2
plt2.clabel( ct_TGM, inline = True , fontsize = 12, fmt = '%1.1f' ) # เขียนค่า N กำกับบนเส้น contour

ct_EGM = plt4.contour( x, y, z2, levels2 ) # plot กราฟ contour ลงในกราฟย่อยที่ 2
plt4.clabel( ct_EGM, inline = True , fontsize = 12, fmt = '%1.1f' ) # เขียนค่า N กำกับบนเส้น contour

ms , index= 0 ,1 # กำหนดค่า mean square และ index เป็นตัวเลข
print( 'number|  lat,lng  |  N_TGM  | N_EGM | diff | diff^2')
for k in range(n):
 for l in range(n):
  diff = z1[k][l] - z2[k][l] # หาผลต่างของ N ทั้งสองแบบจำลอง
  print(  '  {}   {},{} {:.2f}   {:.2f}   {:.2f}    {:.2f} '.format(str(index).ljust(2)\
        , str(LATS[k]).ljust(5), str(LNGS[l]).ljust(6), z1[k][l], z2[k][l], diff, diff**2 ))
  # จัดรูปเพื่อการแสดงผลที่เป็นระเบียบ
  ms, index = ms+diff**2, index + 1 # เพิ่มค่า diff**2 บวกเข้าไปใน ms เพื่อ เก็บค่าามสูตร

rmst = (ms/n**2)**0.5 # คำนวณตามสูตร
    
print('root mean sqrt  error = ', rmst )
plt.show() # แสดงกราฟ