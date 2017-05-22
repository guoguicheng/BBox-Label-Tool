# -*- coding:utf-8 -*-
from PIL import Image, ImageTk
import json,os
import xml.dom.minidom
import random
import shutil
import argparse
Gimagelist=[]
def loadClass():
    with open('classify.json', 'r') as f:
        data = json.load(f)
    return data
def getImages(classify,extArr=['.jpg','.jpeg']):
    fileList=[]
    for filename in os.listdir("Images/%s" %(classify)):
        if os.path.splitext(filename)[1] in extArr:
            fileList.append(filename)
    return fileList
def writeXML(classify,className,imageList):
    global Gimagelist
    rootDir='VOCdevkit'
    VOCdevkitAnnotations=rootDir+'/Annotations'
    VOCdevkitImageSetsMain=rootDir+'/ImageSets/Main'
    VOCdevkitJPEGImages=rootDir+'/JPEGImages'
    for img in imageList:
        im=Image.open('Images/%s/%s' %(classify,img))
        #if im.size[0]<100 or im.size[1]<100:
        #    imageList.remove(img)
        #    continue
        doc=xml.dom.minidom.Document()
        root=doc.createElement('annotation')
        doc.appendChild(root)
        
        folder=doc.createElement('folder')
        folder.appendChild(doc.createTextNode('VOC2007'))
        filename=doc.createElement('filename')
        filename.appendChild(doc.createTextNode(img))
        source=doc.createElement('source')
        
        root.appendChild(folder)
        root.appendChild(filename)
        root.appendChild(source)
        
        database=doc.createElement('database')
        database.appendChild(doc.createTextNode("The VOC2007 Database"))
        annotation=doc.createElement('annotation')
        annotation.appendChild(doc.createTextNode("PASCAL VOC2007"))
        image=doc.createElement('image')
        image.appendChild(doc.createTextNode("flickr"))
        flickrid=doc.createElement('flickrid')
        flickrid.appendChild(doc.createTextNode("341012865"))
        
        
        source.appendChild(database)
        source.appendChild(annotation)
        source.appendChild(image)
        source.appendChild(flickrid)
        
        owner=doc.createElement('owner')
        root.appendChild(owner)
        
        flickrid=doc.createElement('flickrid')
        flickrid.appendChild(doc.createTextNode("Fried Camels"))
        name=doc.createElement('name')
        name.appendChild(doc.createTextNode(''))
        owner.appendChild(flickrid)
        owner.appendChild(name)
        
        size=doc.createElement('size')
        root.appendChild(size)
        
        width=doc.createElement('width')
        width.appendChild(doc.createTextNode(str(im.size[0])))
        height=doc.createElement('height')
        height.appendChild(doc.createTextNode(str(im.size[1])))
        depth=doc.createElement('depth')
        depth.appendChild(doc.createTextNode("3" if im.mode=='RGB' else "2"))
        size.appendChild(width)
        size.appendChild(height)
        size.appendChild(depth)
        
        segmented=doc.createElement('segmented')
        segmented.appendChild(doc.createTextNode("0"))
        root.appendChild(segmented)
        
        box=loadBndbox(classify,img)
        for row in box:
            object=doc.createElement('object')
            root.appendChild(object)
            
            name=doc.createElement('name')
            name.appendChild(doc.createTextNode(className))
            pose=doc.createElement('pose')
            pose.appendChild(doc.createTextNode(""))
            truncated=doc.createElement('truncated')
            truncated.appendChild(doc.createTextNode("0"))
            difficult=doc.createElement('difficult')
            difficult.appendChild(doc.createTextNode("0"))
            object.appendChild(name)
            object.appendChild(pose)
            object.appendChild(truncated)
            object.appendChild(difficult)
            bndbox=doc.createElement('bndbox')
            object.appendChild(bndbox)
        
            xmin=doc.createElement('xmin')
            xmin.appendChild(doc.createTextNode(str(int(row[0]))))
            ymin=doc.createElement('ymin')
            ymin.appendChild(doc.createTextNode(str(int(row[1]))))
            xmax=doc.createElement('xmax')
            xmax.appendChild(doc.createTextNode(str(int(row[2]))))
            ymax=doc.createElement('ymax')
            ymax.appendChild(doc.createTextNode(str(int(row[3]))))
            bndbox.appendChild(xmin)
            bndbox.appendChild(ymin)
            bndbox.appendChild(xmax)
            bndbox.appendChild(ymax)
        shutil.copy('Images/%s/%s' %(classify,img),VOCdevkitJPEGImages)
        #print (img);
        fp = open(VOCdevkitAnnotations+"/"+os.path.splitext(img)[0]+".xml", 'w')
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
        #quit()
    Gimagelist.append(imageList)
def loadBndbox(classify,imgName):
    Bndbox=[]
    f=open('Labels/%s/%s.txt' %(classify,os.path.splitext(imgName)[0]), 'r')
    line=f.readline()
    i=0
    while(line):
        if i==0:
            line=f.readline()
            i+=1
            continue
        Bndbox.append(line.split(' '))
        line=f.readline()
        i+=1
    return Bndbox
def createImageSets():
    global Gimagelist
    for imagelist in Gimagelist:
        random.shuffle(imagelist)
        test_redio=0.5
        trainval_redio=0.5
        val_redio=0.5
        train_redio=0.5
        test=imagelist[:int(len(imagelist)*test_redio)]
        trainval=imagelist[-int(len(imagelist)*trainval_redio):]
        train=trainval[:int(len(trainval)*train_redio)]
        val=trainval[-int(len(trainval)*val_redio):]
        fptest = open("VOCdevkit/ImageSets/Main/test.txt", 'w')
        for line in test:
            fptest.write(os.path.splitext(line)[0]+'\n')
        fptrainval = open("VOCdevkit/ImageSets/Main/trainval.txt", 'w')
        for line in trainval:
            fptrainval.write(os.path.splitext(line)[0]+'\n')
        fptrain = open("VOCdevkit/ImageSets/Main/train.txt", 'w')
        for line in train:
            fptrain.write(os.path.splitext(line)[0]+'\n')
        fpval = open("VOCdevkit/ImageSets/Main/val.txt", 'w')
        for line in val:
            fpval.write(os.path.splitext(line)[0]+'\n')
 
def main():
    parser = argparse.ArgumentParser(description='train an image classifer on imagenet')
    parser.add_argument('--ext', type=str, default='.JPEG',help='[.jpg|.png|...]')
    args = parser.parse_args()
    imgExt=args.ext
    classList=loadClass()
    print(classList)
    for cla in classList:
        print cla
        imglist = getImages(cla,extArr=[imgExt])
        #print imglist
        writeXML(cla,classList[cla],imglist)
    createImageSets()
if __name__=="__main__":
    main()