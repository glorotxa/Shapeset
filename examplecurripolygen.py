# How to create a curridata instance with the polygon generator (shapeset)
import pygame
from curridata import *
from buildfeaturespolygon import *
from polygongen import *

n=20
m=5

genparams = {'inv_chance' : 0.5, 'img_shape' : (32,32), 'n_vert_list' : [3,4,30], 'fg_min' : 0.55, 'fg_max' : 1.0,\
        'bg_min' :0.0, 'bg_max': 0.45, 'rot_min' : 0.0, 'rot_max' : 1, 'pos_min' : 0, 'pos_max' : 1, \
        'scale_min' : 0.2, 'scale_max':0.8, 'rotation_resolution' : 255,\
        'nb_poly_max' :2, 'nb_poly_min' :1, 'overlap_max' : 0.5, 'poly_type' :2, 'rejectionmax' : 50,\
        'overlap_bool':True}
    
#genparams2 = {'poly_type' :2,'rot_max' : 1}

datagenerator=Polygongen
funclist =[buildimage,buildedgesangle,builddepthmap,buildidentity,buildsegmentation,output,buildedgesanglec]
dependencies = [None,{'segmentation':4},None,None,{'depthmap':2},None,{'segmentation':4}]
funcparams={'neighbor':'V8','gaussfiltbool' : False, 'sigma' : 0.5 , 'size': 5, 'neg' : True}
nfeatures = 6
batchsize = n*m
seed = 1

curridata=Curridata(nfeatures,datagenerator,genparams,funclist,dependencies,funcparams,batchsize,seed)
#curridata.changegenparam(genparams2)

#------------------------------------------------------------------------------------------------

# To draw with pygame

pygame.display.init()

screen = pygame.display.set_mode((n*genparams['img_shape'][0]*2,m*genparams['img_shape'][1]*6),0,8)

anglcolorpalette=[(0,0,0)]+[(0,0,255)]+[(0,255,0)]+[(255,0,0)]+[(255,255,0)]+\
    [(x,x,x) for x in xrange(5,256)]
screen.set_palette(anglcolorpalette)

it = 0
nmult = 4
if funcparams['neighbor'] is 'V4':
    nmult = 2

def showresult(it):
    curridata.next()
    
    xvalid = (numpy.reshape((curridata.image+1)*0.5*255,\
                            (batchsize,genparams['img_shape'][0],genparams['img_shape'][1]))/255.0*250+5)
    yvalid = numpy.reshape((curridata.edges+1)*0.5, (batchsize,4,genparams['img_shape'][0],genparams['img_shape'][1]))
    zvalid = (numpy.reshape((curridata.depth+1)*0.5*255, \
                            (batchsize,genparams['img_shape'][0],genparams['img_shape'][1]))/255.0*250+5)
    wvalid = numpy.reshape((curridata.identity+1)*0.5, \
                            (batchsize,len(genparams['n_vert_list']),genparams['img_shape'][0],genparams['img_shape'][1]))
    svalid = numpy.reshape((curridata.segmentation+1)*0.5*255, \
                            (batchsize,genparams['img_shape'][0]*nmult,genparams['img_shape'][1]))
    tvalid = (numpy.reshape((curridata.edgesc+1)*0.5*255,\
                            (batchsize,4,genparams['img_shape'][0],genparams['img_shape'][1]))/255.0*250+5)
    
    for j in range(batchsize):
        xi = (j/m)*genparams['img_shape'][0]*2
        yi = (j-(j/m)*m)*genparams['img_shape'][1]*6
        print xi,yi
        
        new=pygame.surfarray.make_surface(xvalid[j,:,:])
        new.set_palette(anglcolorpalette)
        screen.blit(new,(xi,yi))
    
        ytmp=(yvalid[j,2,:,:]*yvalid[j,3,:,:])*4 + (yvalid[j,0,:,:]*yvalid[j,3,:,:])*1\
            +(yvalid[j,0,:,:]*yvalid[j,1,:,:])*2 + (yvalid[j,1,:,:]*yvalid[j,2,:,:])*3
        new=pygame.surfarray.make_surface(ytmp)
        new.set_palette(anglcolorpalette)
        screen.blit(new,(xi+genparams['img_shape'][0],yi+0))
    
        new=pygame.surfarray.make_surface(zvalid[j,:,:])
        new.set_palette(anglcolorpalette)
        screen.blit(new,(xi+0,yi+genparams['img_shape'][1]))
    
        ytmp=wvalid[j,0,:,:]*1+wvalid[j,1,:,:]*2+wvalid[j,2,:,:]*3
        new=pygame.surfarray.make_surface(ytmp)
        new.set_palette(anglcolorpalette)
        screen.blit(new,(xi+genparams['img_shape'][0],yi+genparams['img_shape'][1]))
    
        new=pygame.surfarray.make_surface(svalid[j,:genparams['img_shape'][0]*2-1,:])
        new.set_palette(anglcolorpalette)
        screen.blit(new,(xi+0,yi+genparams['img_shape'][1]*2))
    
        if nmult != 2:
            new=pygame.surfarray.make_surface(svalid[j,genparams['img_shape'][0]*2:genparams['img_shape'][0]*4-1,:])
            new.set_palette(anglcolorpalette)
            screen.blit(new,(xi+0,yi+genparams['img_shape'][1]*3))
    
        new=pygame.surfarray.make_surface(tvalid[j,2,:,:])
        new.set_palette(anglcolorpalette)
        screen.blit(new,(xi+0,yi+genparams['img_shape'][1]*4))
    
        new=pygame.surfarray.make_surface(tvalid[j,0,:,:])
        new.set_palette(anglcolorpalette)
        screen.blit(new,(xi+genparams['img_shape'][0],yi+genparams['img_shape'][1]*4))
    
        new=pygame.surfarray.make_surface(tvalid[j,1,:,:])
        new.set_palette(anglcolorpalette)
        screen.blit(new,(xi+0,yi+genparams['img_shape'][1]*5))
    
        new=pygame.surfarray.make_surface(tvalid[j,3,:,:])
        new.set_palette(anglcolorpalette)
        screen.blit(new,(xi+genparams['img_shape'][0],yi+genparams['img_shape'][1]*5))
    
        pygame.display.update()
        print curridata.output[j,:]
        #raw_input("Please press Enter")
    it += 1
    print it
    return it
    #raw_input("Please press Enter")

#------------------------------------------------------------------------------------------------

#to test with timeit

from timeit import Timer

def genex(curridata,n,mode=1):
    it = 0
    while it<n:
        if mode:
            curridata.image
            curridata.segmentation
            curridata.edges
            curridata.depth
            curridata.identity
            curridata.output
        curridata.next()
        it+=1
        #print it

#tim1=Timer("genex(curridata,1000,1)","from __main__ import genex, curridata ; gc.enable()").timeit(1)
#tim2=Timer("genex(curridata,1000,0)","from __main__ import genex, curridata ; gc.enable()").timeit(1)

#------------------------------------------------------------------------------------------------


#curridata.gen.rot_min=0
it =showresult(it)

#pygame.display.quit()