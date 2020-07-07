import numpy as np 


P1=(632,320)
P2=(610,355)
pixel_diff=pixel_diff_y= np.sqrt((P1[0]-P2[0])**2+(P1[1]-P2[1])**2)
#print(pixel_diff)
coor_diff=coor_diff_y = 0.000005 # real distance = 0.005km= 5m 
res =(843,1500)
H=res[0]
W=res[1]
center=(421,750)


P3=(390,50)
P4=(680,56)
coor_diff_x=0.000004 # real distance = 4m
pixel_diff_x=np.sqrt((P3[0]-P4[0])**2+(P3[1]-P4[1])**2)

D_angle=34.94272545176713
angle=0.6098656087537595
print(pixel_diff_y/coor_diff_y)
print(pixel_diff_x/coor_diff_x)



f1=19
p1=(730,65)
gps1=(24.7676, 55.3706)

f2=25
p2=(725,680)
gps2=(24.7676, 55.37068571428571)

pixel_diff_y=(680-65)
coor_diff_y=(gps2[1]-gps1[1])

print((680-65)*coor_diff_y/pixel_diff_y)
print((gps2[1]-gps1[1]))

def rotate(coor,angle):
    x=coor[0]*np.cos(angle)-coor[1]*np.sin(angle)
    y=coor[0]*np.sin(angle)+coor[1]*np.cos(angle)
    return(x,y)


Origin=(3287.405407641197, 4760.116207756659)
angle= 0.6098656087537595
p1=(730,46)
f1=575
gps1=(3287.3963056583584, 4760.125437593168)
gps1=rotate(gps1,angle)
p2=(730,642)
f2=749
gps2=(3287.3893780198873, 4760.130221890971)
gps2=rotate(gps2,angle)
coor_diff_y=np.sqrt((gps1[0]-gps2[0])**2+(gps1[1]-gps2[1])**2)
pixel_diff_y=642-46
pixel_diff_x=pixel_diff_y*W/H
coor_diff_x=coor_diff_y
#pixel_diff_y=(642,46)

def cart_to_pixel(displacement,H=H,W=W):
    X_loc= min(int(displacement[0]*pixel_diff_x/coor_diff_x),W)
    Y_loc= min(int(displacement[1]*pixel_diff_y/coor_diff_y),H)
    return(X_loc,Y_loc)


def rotate(coor,angle):
    x=coor[0]*np.cos(angle)-coor[1]*np.sin(angle)
    y=coor[0]*np.sin(angle)+coor[1]*np.cos(angle)
    return(x,y)

def pixel_to_cart(loc):
    #x_norm =(loc[0]//50)*50 + 25
    #y_norm =(loc[1]//102)*102 + 51
    (x_norm,y_norm)=((loc[0]-center[0]),(loc[1]-center[1]))
    #D=np.sqrt((x_norm-center[0])**2+(y_norm-center[1])**2)
    #loc_angle=np.arctan(abs((y_norm-center[1]))-abs((x_norm-center[0])))
    x=(x_norm)*coor_diff_x/pixel_diff_x
    y=(y_norm)*coor_diff_y/pixel_diff_y
    #x=x_norm*np.cos(angle)-y_norm*np.sin(angle)
    #y=x_norm*np.sin(angle)+angley_norm*np.cos(angle)
    #print(x,y)
    return( (x,y))

def unique_id(loc,gps_coor):
    Origin=(3287.405407641197, 4760.116207756659)
    angle= np.pi/2 - 0.6098656087537595
    #Origin=rotate(Origin,angle)
    (x_coor,y_coor)=pixel_to_cart(loc)
    #gps_coor=rotate(gps_coor,angle)
    X_loc,Y_loc =  (gps_coor[0]-x_coor,gps_coor[1]-y_coor)

    X_loc-=Origin[0]
    Y_loc-=Origin[1]
    
    X_loc*=10000
    Y_loc*=10000
    print(X_loc,Y_loc)

    #X_loc//=102
    #Y_loc//=102
    return(round(X_loc),round(Y_loc))
def unique_id_old_2(loc,gps_coor):
    (x_coor,y_coor)=pixel_to_cart(loc)
    X_loc,Y_loc =  (gps_coor[0]+x_coor,gps_coor[1]-y_coor)
    Y_loc-=3287.405407641197
    X_loc-=4760.116207756659
    X_loc*=10000
    Y_loc*=10000
    #X_loc//=102
    #Y_loc//=102
    return(round(X_loc),round(Y_loc))

def unique_id_new(loc,gps_coor):
    Origin=(24.7676, 55.3705)
    #print()
    (x_coor,y_coor)=pixel_to_cart(loc)
    #(x_coor,y_coor)=pixel_to_cart(loc)
    #X_loc,Y_loc =  (gps_coor[0],gps_coor[1])
    X_loc,Y_loc =  (x_coor,y_coor)

    X_loc*=1000000
    Y_loc*=1000000
    X_loc+=(-Origin[0]+gps_coor[0])*1000000
    Y_loc-=(-Origin[1]+gps_coor[1])*1000000
    return(round(X_loc),round(Y_loc))

def shift(loc,point):
    s=pixel_to_cart(point)
    return(loc[0]+s[0],loc[1]+s[1])
    
print(unique_id(p1,gps1))
print(unique_id(p2,gps2))

'''
f1=633
f2=825
actual_distance= 9
p1=(3287.3939964463084, 4760.127032360222)
p2=(3287.3863521526223, 4760.132311581102)
diff=np.sqrt((p1[0]-p2[0])**2 +((p1[1]-p2[1])**2 ))
print(diff) # should be around 9 meters
'''

box=(1018,165,1126,250)
x=box[0]
y=box[1]
W=box[2]-box[0]
H=box[3]-box[1]
aspect_ratio=H/W
area=H*W

print(aspect_ratio)
print(area)