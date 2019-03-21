import cv2                              
import numpy as np
import math
import random
import os
#import serial
import time
#ser = serial.Serial("",9600)
count1=0;
a1=0;
count2=0;
a2=0;
ar=[0,0,0,0,0,0];
comp_tot = 0
play_tot = 0
num1 = random.randrange(0,6);
rand = 0
videoFrame = cv2.VideoCapture(-1)
def fingercount():
    min_YCrCb = np.array([0,133,77],np.uint8)
    max_YCrCb = np.array([255,173,127],np.uint8)
    x=0
    y = range(70)
    r = range(7)
    r = [0,0,0,0,0,0,0]
    t = 0
    dis = range(8)
    q =range(2)
    keyPressed = -1 

    while(keyPressed < 0): 
        readSucsess, img = videoFrame.read()

        imageYCrCb = cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)

        blur = cv2.GaussianBlur(imageYCrCb,(3,3),0)

        skinRegion = cv2.inRange(blur,min_YCrCb,max_YCrCb)

        contours, hierarchy = cv2.findContours(skinRegion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        drawing = np.zeros(img.shape,np.uint8)
        max_area=0
        ci=0
        while (len(contours)==0):
            if len(contours)!=0:
                break
        for i in range(len(contours)):
                cnt=contours[i]
                area = cv2.contourArea(cnt)
                if(area>max_area):
                    max_area=area
                    ci=i
        cnt=contours[ci]
        hull = cv2.convexHull(cnt)
        moments = cv2.moments(cnt)
        if moments['m00']!=0:
                    cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                    cy = int(moments['m01']/moments['m00']) # cy = M01/M00
        centr=(cx,cy)       
        cv2.circle(drawing,centr,5,[0,0,255],2)       
        cv2.drawContours(drawing,[cnt],0,(0,255,0),2) 
        cv2.drawContours(drawing,[hull],0,(0,0,255),2) 
        cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        hull = cv2.convexHull(cnt,returnPoints = False)
        j=0
        if(1):
                   defects = cv2.convexityDefects(cnt,hull)
                   if defects == None :
                       print 'Hand not shown'
                       t=1
                       continue
                   for i in range(defects.shape[0]):
                        s,e,f,d = defects[i,0]
                        start = tuple(cnt[s][0])
                        end = tuple(cnt[e][0])
                        far = tuple(cnt[f][0])
                        dist = cv2.pointPolygonTest(cnt,centr,True)
                        cv2.line(drawing,start,end,[0,255,0],2)                    
                        n = math.sqrt(((start[0]-end[0])*(start[0]-end[0]))+((start[1]-end[1])*(start[1]-end[1])))
                        angle=(math.atan2(cy-start[1],cx-start[0])*180)/math.pi
                        if n < 165 :
                            if n > 40 :
                                cv2.circle(drawing,end,5,[0,0,255],-1)
                                j = j+1
                                q[0] = end[0]
                                q[1] = end[1]
                   j = j+1
                   if j == 2:
                    
                       cv2.circle(drawing,centr,int(0.0045*max_area),[0,0,255],2)
                       yi = math.sqrt(((q[0]-cx)*(q[0]-cx))+((q[1]-cy)*(q[1]-cy)))
                       #print yi
                       if yi < int(0.0045*max_area) :
                           j=6
                       #if angle < 0  :
                           #if angle > -100:
                               #j=6 
                   if x < 50 :
                        x = x+1
                        y[x] = j
                   else:
                        x=0
                   i=0
        cv2.imshow('drawing',drawing)
        cv2.imshow('img',img)
        if t == 1:
            t = 0
            continue
        if x < 50 :
            if y[x] == 0:
                   r[0] = r[0]+1;
            if y[x] == 1:
                    r[1] = r[1]+1;
            if y[x] == 2:
                    r[2] = r[2]+1;
            if y[x] == 3:
                    r[3] = r[3]+1;
            if y[x] == 4:
                    r[4] = r[4]+1;
            if y[x] == 5:
                    r[5] = r[5]+1;
            if y[x] == 6:
                    r[6] = r[6]+1;
            x = x+1
                
        elif x ==50:
            x=0
            i=1
            tmax = r[0]
            index = 0
            while(i<=6):
                if r[i] > tmax:
                    tmax=r[i]
                    index = i
                i = i+1
            
            r= [0,0,0,0,0,0,0]
            #print "Finger shown" 
            #print index
            return index        
        k = cv2.waitKey(10)
        if k == 27:
            break
    videoFrame.release()
def cls():
    print "\n" * 10
def randomgen():
    k=random.randrange(0,6);
    return k;
def collect_bat(val):
    global a1
    global rand
    out=randomgen()
    if val-a1==0 and out==val:
        if out==6:
            out-=1
        else:
            out+=1
    a1=val
    print "Roboarm value:"
    print out+1
    rand = out+1
def collect_bowl(val):
    global ar
    global a2
    out=0
    global count2;
    count2+=1
    b=ar[0];
    
    for i in range(1,5):
        if ar[i]>b:
            b=ar[i]
            out=i
    if  count2%4==0 or count2%7==0 or count2==1:
        out=randomgen()
    if count2%10==0:
        for m in range(0,5):
            ar[m]=0
    if val-a2==1:
            out=a2
    print out+1
    rand = out+1
    a2=val
    ar[val-1]+=1
while (True) :
    print "BATTING"
    while (True):
        global rand
        global num1
        collect_bat(num1)
        print "Number Shown:"
        num=fingercount()
        print num
        num1 = num
        #import time
        #time.sleep(1)
        if num == rand :
            print "The Arm is out"
            print "The Arm's score is :"
            print comp_tot
            temp = cv2.waitKey(2000)
            time.sleep(3)
            cls()
            break
        else :
            comp_tot = comp_tot + rand
        #cls()
    print "BOWLING"
    while (True) :
        collect_bowl(num1)
        print "getting number:"
        num=fingercount()
        print num
        num1 = num
        if num == rand :
            print "The Player is out"
            print "The Player's score is :"
            print play_tot
            if comp_tot > play_tot:
                print "The Arm wins"
            elif comp_tot == play_tot :
                print "The game is a Tie"
            time.sleep(5)
            #cv2.waitkey(2000)
            cls()
            break
        else :
            play_tot = play_tot + num
        if play_tot > comp_tot :
            print "The Player wins"
            #cv2.waitkey(2000)
            time.sleep(5)
            cls()
            break
        #import time
        #time.sleep(3)
        #cls()
    esc = cv2.waitKey(10)
    if esc == 27 :
        break
    
cv2.destroyAllWindows()

