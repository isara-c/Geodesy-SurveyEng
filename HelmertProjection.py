# Problem : Helmert Projection


import math as m

AMS = [ 52.308613, 4.763889, -11] # ใส่ค่าพิกัดลงและความสูงลงใน AMS
BAH = [ 26.270833, 50.633611, 6 ] # ใส่ค่าพิกัดลงและความสูงลงในBAH

def Geodetic2Cartesian(P,L,h): # ฟังก์ชันที่แปลงจาก Geodetic มาเป็น Cartesian
    h *= 0.3048 # แปลงจากฟุตเป็นเมตร
    a,f = 6378137, 1/298.25722356 # ค่า a และ f ในระบบ WGS84
    b = a*(1-f)
    e = 1-(b**2/a**2)
    N = (a/m.sqrt(1-(e**2)*(m.sin(m.radians(P))**2))) # คำนวณ N ตามสูตร
    X = (N+h)*m.cos(m.radians(P))*m.cos(m.radians(L)) # คำนวณ X ตามสูตร
    Y = (N+h)*m.cos(m.radians(P))*m.sin(m.radians(L)) # คำนวณ Y ตามสูตร
    Z = ((1-e**2)*N+h)*m.sin(m.radians(P)) # คำนวณ Z ตามสูตร
    return(X,Y,Z) # คืนค่า cartesian X, Y, Z ทั้งสามออกมา

def Cartesian2Geodetic(X,Y,Z): # ฟังก์ชันที่แปลงจาก Cateian มาเป็น Geodetic
    a,f = 6378137, 1/298.25722356  # ค่า a และ f ในระบบ WGS84
    b = a*(1-f)
    e = 1-(b**2/a**2)
    P = m.atan(Z/m.sqrt(X**2+Y**2)) # คำนวณจาก X Y  Z กลับไปเป็นละติจูด
    fP = m.tan(P)-(Z+((e**2)*(a/(m.sqrt(1-(e**2)*(m.sin(P))**2)))*m.sin(P)))/(m.sqrt(X**2+Y**2))
    fPd = ((1/m.cos(P))**2)-(((e**2)*a*m.cos(P))/(((1-(e**2)*((m.sin(P))**2))*1.5)*(m.sqrt(X**2+Y**2))))
    P -= fP/fPd
    N = (a/m.sqrt(1-(e**2)*(m.sin((P))**2))) # คำนวณ N เพื่อใช้ในการหา h
    L = m.atan(Y/X)  # คำนวณค่าลองจิจูดจากสูตร
    h = (m.sqrt(X**2+Y**2)/m.cos(P))-N # คำนวณค่า h จากสูตร
    return(m.degrees(P),m.degrees(L),h)

print( 'Cartesian of AMS = (X, Y, Z) = {:}'.format(Geodetic2Cartesian(AMS[0], AMS[1], AMS[2]) ))
# ใช้ฟังก์ชันแปลง AMS เป็น cartesian(X, Y, Z)
x, y, z = Geodetic2Cartesian(AMS[0], AMS[1], AMS[2]) # แก้ไข

print( 'Geodetic of AMS = (P, L, h) = {:}'.format(Cartesian2Geodetic(x, y, z)))

print( 'Cartesian of BAH = (X, Y, Z) = {:}'.format(Geodetic2Cartesian(BAH[0], BAH[1], BAH[2]) ))
# ใช้ฟังก์ชันแปลง BAH เป็น cartesian(X, Y, Z)

x , y, z= Geodetic2Cartesian(BAH[0], BAH[1], BAH[2]) # แก้ไข

print( 'Geodetic of BAH = (P, L, h) = {:}'.format(Cartesian2Geodetic(x, y, z)))
