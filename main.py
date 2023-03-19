import threading
from time import sleep
from pynput.keyboard import Key, Listener
import pyautogui as pag
import numpy as np
import cv2 as cv


Whites = []
WIMG   = ""

def record():
    img_bgr = pag.screenshot()
    img_bgr = np.array(img_bgr)
    img_rgb = img_bgr[:,:,::-1].copy()
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread('obj/' + WIMG + '.jpg',0)
    w, h = template.shape[::-1]
    
    res = cv.matchTemplate(img_gray, template,cv.TM_SQDIFF_NORMED)
    mn,mx,mnLoc,mxLoc = cv.minMaxLoc(res)
    
    print(mx)
    threshold = 0.05
    loc = np.where(res <= threshold)
    points = []
    for pt in zip(*loc[::-1]):
        close = False
        for p in points:
            if abs(pt[0] - p[0]) < 10 and abs(pt[1] - p[1]) < 10:
                close = True
                break
        
        if close: 
            continue
        points.append(pt)
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    
    global Whites
    Whites = points


def go():
    global Whites
    print(Whites)
    for pt in Whites:
        pag.click(pt[0] + 30, pt[1] + 30)
        sleep(0.05)

def kb_listener():
    def on_release(key):
        print(str(key))
        if str(key) == "<79>":
            record()
        elif str(key) == "<80>":
            go()

    with Listener(on_release=on_release) as listener:
        listener.join()
    

if __name__ == '__main__':
    WIMG = input("Type 7 for 7x7, 8 for 8x8 then press Enter\n")
    if not (WIMG in ("7", "8")):
        print("Type either 7 or 8 to run this bot, Exiting...")
        quit()
		
    print("Running...")
	
    while True:
        kb_listener()
