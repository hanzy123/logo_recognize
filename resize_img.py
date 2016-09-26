# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 18:35:32 2016

@author: mac
"""

from PIL import Image   
    
     
f = open("logo_path.txt", "r")  
while True:  
    line = f.readline()  
    line = line[:-1]
    if line:  
        img = Image.open(line)
        new_img = img.resize((128,128),Image.BILINEAR)
        new_img.save(line)
        print("deal " + line)
    else:  
        break
f.close()