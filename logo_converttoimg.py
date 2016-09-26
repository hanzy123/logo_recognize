# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 09:36:56 2016

@author: mac
"""
import imghdr
import os

def writepathtotxt(data_sets):
    txt_path = 'logo_path.txt'
    with open(txt_path,"w") as f:
        for data_set in data_sets:
            f.write(data_set)
            f.write('\n')
def processDirectory (args,dirname,filenames):
    for filename in filenames:
        if filename == '.DS_Store':
            continue
        else:
            file_paths.append(dirname + '/' + filename)
def converttoimg(imgType,imgpath):
    if imgType == 'png':
        order = 'convert ' +  imgpath + ' ' + imgpath[:-3] + 'jpg'      
        os.system(order)
        if file_path[-3:] == 'jpg':        
            data_sets.append('/Users/mac/python_work/getlogo/'+file_path)
    elif imgType == 'tiff':
        order = 'convert ' +  imgpath + ' ' + imgpath[:-4] + 'jpg'      
        os.system(order)
        if file_path[-3:] == 'jpg':
            data_sets.append('/Users/mac/python_work/getlogo/'+file_path)
if __name__ == "__main__":
    file_paths = []
    data_sets = []#成功转成jpg格式的图片路径
    global file_paths,data_sets
    os.path.walk(r'logo_img/', processDirectory, None )
    for file_path in file_paths:   
        try:
            imgType = imghdr.what(file_path)#获取图片格式
            #if imgType == 'png' or imgType == 'tiff':     
                #converttoimg(imgType,file_path)
            if imgType == 'jpeg' and file_path[-3:] == 'jpg':
                data_sets.append('/Users/mac/python_work/getlogo/'+file_path)
        except:
            continue
    print "image convert Down!"
    writepathtotxt(data_sets)
    print "path_file generate"