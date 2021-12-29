import cv2
import numpy as np
import pandas as pd
import math

#Reading the image with opencv
img = cv2.imread('tree.png')

clicked = False
r = g = b = xpos = ypos = 0

#Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)


#function to calculate minimum distance from all colors and get the most matching color
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"]))**2 + abs(G- int(csv.loc[i,"G"]))**2+ abs(B- int(csv.loc[i,"B"]))**2
        d=math.sqrt(d)
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]+' '+csv.loc[i,"hex"]
    return cname


#function to get x,y coordinates of mouse double click
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
       
cv2.namedWindow('Color Detector')
cv2.setMouseCallback('Color Detector',draw_function)

while(1):

    cv2.imshow('Color Detector',img)
    if (clicked):
        
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        #Creating text string to display( Color name, hex code and RGB values )
        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        #For very light colours display text in black colour otherwise white color
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),0,0.7,(0,0,0),1,cv2.LINE_AA,False)
        else:
            cv2.putText(img, text,(50,50),0,0.7,(255,255,255),1,cv2.LINE_AA,False)
            
        clicked=False

    #Break the loop when user hits 'esc' key or 'q' key   
    if cv2.waitKey(20)==27 or cv2.waitKey(20)==ord('q'):
        break
    
cv2.destroyAllWindows()
