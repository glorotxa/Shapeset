import pygame


from curridata import *
from buildfeaturespolygon import *
from polygongen import *



################################# INITIALIZATION - Shapeset-3*2 ###############################


# initialization of the common generation parameters (cf polygongen.Polygongen.__init__). 
genparams = {'inv_chance' : 0.5, 'img_shape' : (32,32), 'n_vert_list' : [3,4,20], 'fg_min' : 0.55, 'fg_max' : 1.0,\
        'bg_min' :0.0, 'bg_max': 0.45, 'rot_min' : 0.0, 'rot_max' : 1, 'pos_min' : 0, 'pos_max' : 1, \
        'scale_min' : 0.2, 'scale_max':0.8, 'rotation_resolution' : 255,\
        'nb_poly_max' :2, 'nb_poly_min' :1, 'overlap_max' : 0.5, 'poly_type' :2, 'rejectionmax' : 50,\
        'overlap_bool':True}
#---------

# this should not be changed for common use
datagenerator=Polygongen
funclist =[buildimage,buildedgesangle,builddepthmap,buildidentity,buildsegmentation,output,buildedgesanglec]
dependencies = [None,{'segmentation':4},None,None,{'depthmap':2},None,{'segmentation':4}]
funcparams={'neighbor':'V8','gaussfiltbool' : False, 'sigma' : 0.5 , 'size': 5}
nfeatures = 6
#------------------

batchsize = 10 # number of images generated at each iteration
seed = 0 # seed initialization, usefull to reproduce data generation 
funcparams.update({'neg':True}) #if True, the pixel values are in the range [-1,1], if False: [0,1]
 
# instance creation of the curridata class 
curridata=Curridata(nfeatures,datagenerator,genparams,funclist,dependencies,funcparams,batchsize,seed)


################################################################################

# ---------------------- How to generate polygon scenes?
print curridata._Curridata__data # no scenes are generated yet 

curridata.next() # this create the 'batchsize' next polygon scenes and store them in curridata._Curridata__data

print curridata._Curridata__data # the encoded format of the different generated scenes 

# ---------------------- How to build and manipulate the corresponding images?

print curridata._Curridata__features # the images are not built yet
curridata.image 
# at the first call of curridata.image: 
#	*** it will create the images
#	*** store them in the corresponding field of curridata._Curridata__features
#	*** return it
# the images are flat: curridata.image -> matrix of shape (batchsize,img_shape[0]*img_shape[1])

print curridata._Curridata__features # the images are built in curridata._Curridata__features[0]

# if you do again:
curridata.image 
# it will not create again the images, but just read from curridata._Curridata__features[0] and return them

# curridata.image is the most important modality, but other images modalities of the same scene can be built similarly
curridata.segmentation
curridata.edges
curridata.depth
curridata.identity

# the target of the image can be obtained similarly with:
curridata.output # this is the count of the polygon type for each image.
print curridata.output[:,0] # number of triangles for each images
print curridata.output[:,1] # number of squares for each images
print curridata.output[:,2] # number of ellipse for each images

# if you want to have one class per configuration of objects (nine different for shapeset 3*2):

def convertout(out):
    target =    0*((out[:,0]==1) * (out[:,1] == 0) * (out[:,2]==0)) +\
                1*((out[:,0]==0) * (out[:,1] == 1) * (out[:,2]==0)) +\
                2*((out[:,0]==0) * (out[:,1] == 0) * (out[:,2]==1)) +\
                3*((out[:,0]==1) * (out[:,1] == 1) * (out[:,2]==0)) +\
                4*((out[:,0]==0) * (out[:,1] == 1) * (out[:,2]==1)) +\
                5*((out[:,0]==1) * (out[:,1] == 0) * (out[:,2]==1)) +\
                6*((out[:,0]==2) * (out[:,1] == 0) * (out[:,2]==0)) +\
                7*((out[:,0]==0) * (out[:,1] == 2) * (out[:,2]==0)) +\
                8*((out[:,0]==0) * (out[:,1] == 0) * (out[:,2]==2))
    return target

print convertout(curridata.output)

# For the next images generation you have to call again:
curridata.next() # it deletes previous stored images:
print curridata._Curridata__features