# Problem : Navigation Route on Great Circle ( Sphere )

import math as m        # นำเข้าฟังก์ชัน math เพื่อคำนวณมุมตรีโกณ
import numpy as np      # นำเข้า numpy เพื่อใช้คำนวณ arc
from geographiclib.geodesic import Geodesic 
# นำเข้าเพื่อใช้หาค่าพิกัดทางภูมิศาสตร์

import matplotlib.pyplot as plt             # นำเข้าเพื่อพลอตกราฟละติจูดและลองจิจูด

lat = { 'AMS_A': 52.308613, 'BAH_B': 26.270833 }
lng = { 'AMS_A': 4.763889, 'BAH_B' : 50.633611 }
# ค่าพิกัดสนามบินจัดเก็บในรูปแบบ dict 

def InverseProblem ( lat1, lng1, lat2, lng2 ):
# คำนวณระยะทางระหว่างสนามบินทั้งสองแห่งแบบ InverseProblem โดยรู้จุดเริ่มต้นและจุดสิ้นสุด

    lat1, lng1, lat2, lng2 = m.radians(lat1), m.radians (lng1), m.radians(lat2), m.radians(lng2)
    # แปลงให้อยู่ในรูป radians เนื่องจากเป็นฟอร์มของไพธอน
    
    s12 = 6371* np.arccos( m.sin( lat1 )* m.sin(  lat2 ) + m.cos( lat1 )* m.cos(  lat2 )* m.cos(  lng1 - lng2 ) )
    # คำนวณระยะทางระหว่างสนามบินตามสูตร

    a , b =  m.radians(90) - lat2 , m.radians(90) - lat1 # ระยะส่วนโค้งของ a และ b เพื่อนำไปคำนวณหาพิกัด

    diff_lng  =  m.radians( s12/6371*180/m.pi )  # ค่าต่างของลองจิจูดทั้งสองสนามบิน
    Az_A = np.arccos( ( m.cos(a) - m.cos(b)*m.cos(diff_lng) ) / ( m.sin(b) * m.sin(diff_lng) ) )
    # คำนวณหา Azimuth ที่จุดเริ่มต้น

    Az_B = np.arccos( ( m.cos(b) - m.cos(a)*m.cos(diff_lng) ) / ( m.sin(diff_lng) * m.sin(a) ) )
    # คำนวณหา Azimuth จุดสิ้นสุด

    return ( m.degrees( Az_A )  ,  180  - m.degrees( Az_B )  , s12 ) 
    # คืนค่าออกมาเป็น Azi ของจุดเริ่มต้น Azi จุดสิ้นสุด และระยะห่างระหว่างสองสนามบิน

def DirectProblem ( lat1, lng1, Az_1, s12 ): # ฟังก์ชันคำนวณ Directproblem โดยทราบพิกัดจุดเริ่มต้นและระยะทาง
    SEGMENTS = np.linspace( 0, s12 , num=11, endpoint=True )
    # แบ่งระยะทาง s12 ออกเป็น 10 ช่วงจะได้ทั้งหมด 11 จุด เพื่อที่จะนำไปคำนวณหาค่าอะซิมุทที่แต่ละจุด
    value_a , value_Az = [] , [] # สร้างลิสท์เพื่อรองรับค่าพิกัดละติจูด และค่าอะซิมุทของแต่ละจุด
    for s in SEGMENTS: # วนลูปโดยเรียงตามค่าระยะทางที่คำนวณได้จาก linspace
        c, b= m.radians( s/6371*180/m.pi ), m.radians( 90 - lat1 ) # หาค่า c และ b ตามความสัมพันธ์
        a = np.arccos( m.cos(b) * m.cos(c) + m.sin(b)*m.sin(c)*m.cos( m.radians( Az_1 )) )
        value_a.append ( a ) # ใส่ค่า a คือพิกัดละติจูด ไว้ใช้หาอะซิมุท ของแต่ละพิกัด
        
    for i in range(11): # วนลูปจำนวน 11 ครั้งเพื่อหาอะซิมุททั้งหมด
        c = m.radians( s12/10*180/m.pi/6371) 
        if i == 10 : # แยกกรณีครั้งสุดท้ายเนื่องจากหากเป็นจุดสุดท้ายจะทำการคิดอะซิมุทโดยอาศัยความสัมพันธ์ cos
            b, a = value_a[i-1], value_a[i] # ใช้ค่า b และ a จากการคำนวณละติจูด
            Az = m.radians(180) - np.arccos( ( m.cos(b) -  m.cos(c)  * m.cos(a) ) / ( m.sin(c) * m.sin(a) ) )
            # หาค่า Az ด้วยวิธี cosine rule
        else: # ใช้ cosine rule เพื่อหาอะซิมุทของแต่ละจุด โดยใช้ข้อมูลคือพิกัดของแต่ละจุด
            b, a = value_a[i] ,value_a[i+1] # ใช้ค่า b และ a ที่ได้จากการคำนวณละติจ
            Az = np.arccos( ( m.cos(a) -  m.cos(c)  * m.cos(b) ) / ( m.sin(c) * m.sin(b) ) )
        value_Az.append ( m.degrees( Az ) ) # เพิ่มค่า Azimuth ลงในลิสท์ที่เตรียมไว้ให้
    return value_Az # คืนค่าอะซิมุทของแต่ละจุดออกมาทั้งหมด


################หาค่า Azimuth และระยะทาง ######################

print( '--------------- ( B. ) Find Azimuth & distance--------------------')
Az_1 = InverseProblem ( lat['AMS_A'], lng['AMS_A'], lat['BAH_B'], lng['BAH_B'] )[0]
# คำนวณ Azimuth ที่จุดเริ่มต้น จากฟังก์ชัน InverseProblem และเก็บไว้ในตัวแปร Az_1

Az_2 = InverseProblem (  lat['AMS_A'], lng['AMS_A'], lat['BAH_B'], lng['BAH_B'] )[1]
# คำนวณ Azimuth ที่จุดสิ้นสุด จากฟังก์ชัน InverseProblem และเก็บไว้ในตัวแปร Az_2

s12 = InverseProblem( lat['AMS_A'], lng['AMS_A'], lat['BAH_B'], lng['BAH_B'] )[2]
print( 'Azimuth AMS', Az_1 , 'in dd') # แสดงผลค่าอซิมุทของสนามบินจุดเริ่มต้น
print( 'Azimuth BAH', Az_2, 'in dd')  # แสดงผลค่าอซิมุทของสนามบินจุดสิ้นสุด
print( 'Distance = ', s12, 'km.', '\n') # แสดงผลค่าระระทางระหว่างสองสนามบิน

################# แบ่งระยะทาง s12 เป็น 10 ช่วง #####################

( '--------------- ( C. ) compare between linspace and 10 period-------------')
geod = Geodesic.WGS84 # ใสประเภทของ Datum ทีใช้คือ WGS84  
geod = Geodesic(6371.0, 0.0) # ใส่ค่ารัศมีโลกโดยมีค่าเท่ากับ 6371 km.

geod_line = geod.InverseLine( 52.308613, 4.763889 ,26.270833  ,50.633611 )
# ใส่ค่าพิกัดลงในตัวแปร โดยใช้คำสั่ง geod.InverseLine โดยค่าพิกัดที่ใส่คือ lat1, lng1, lat2, lng2

SEGMENTS = np.linspace( 0, geod_line.s13 , num=11, endpoint=True ) # แบ่งระยะออกเป็น 10 ช่วง จะได้ทั้งหมด 11 จุด
for i in range(11): # แสดงระยะที่แบ่งเป็นช่วงทั้งหมด
    print( 's{:.0f} = {:.5f} km.'.format(i+1,SEGMENTS[i]))# แสดงระยะที่แบ่งเป็นช่วงทั้งหมด
print( 's12 / 10 =  {:.5f}'.format( s12 / 10 ) , 'km.' , '\n' ) # นำมาเปรียบเทียบกับค่าที่ได้จาก linspace 
#############เปรียบเทียบอะซิมุทที่ได้ด้วยวิธี Direct ###################

print( '--------------- ( D. ) Direct Problem to find Az-------------------------')
all_az = DirectProblem ( lat['AMS_A'], lng['AMS_A'], Az_1, s12 )
for j in range(11): # แสดงระยะที่แบ่งเป็นช่วงทั้งหมด
    print( 'Az{:.0f} = {:.5f}'.format(j+1,all_az[j]))

####################### Geographiclib ########################

print( '--------------- ( E. ) Geographiclib geod.InverseLine--------------------')
lats = [] ; lngs = [] ; az2s = [] # สร้างลิสท์ไว้เก็บข้อมูล
print( "| =distance= | =latitude= | =longitude= | ==azimuth== |" )
# แสดงค่าที่ได้จาก Module geographiclib.geodesic 
for seg in SEGMENTS:# หาค่าละติจูด ลองจิจูดเพื่อนำไปพลอตกราฟ
    pos = geod_line.Position(seg, Geodesic.STANDARD | Geodesic.LONG_UNROLL)
    # Geodesic.LONG_UNROLL ไม่ให้ค่าติดลบ จะได้ค่าเป็น 0-360
    lats.append( pos['lat2'] ) # เพิ่มค่าละติจูดลงในลิสท์ lats
    lngs.append( pos['lon2'] ) # เพิ่มค่าลองจิจูดลงในลิสท์ lngs
    az2s.append( '{:.1f}'.format( pos['azi2'] ) ) # เพิ่มค่า Azimuth แต่ละจุดลงในลิสท์
    print( "| {:10.0f} | {:10.5f} | {:10.5f}  | {:10.5f} |".format(\
         pos['s12'], pos['lat2'], pos['lon2'], pos['azi2'] ) )
    # แสดงค่าระยะทาง ละติจุด ลองจิจูด และอะซิมุทของแต่ละจุด
