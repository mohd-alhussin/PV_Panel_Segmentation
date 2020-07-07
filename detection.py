#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip uninstall -y keras


# # Mask R-CNN Demo
# 
# A quick intro to using the pre-trained model to detect and segment objects.

# In[2]:


import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
import cv2
import os
# Root directory of the project
ROOT_DIR = os.path.abspath("../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
#os.system("pwd")
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
import coco

#get_ipython().run_line_magic('matplotlib', 'inline')

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "images")


# ## Configurations
# 
# We'll be using a model trained on the MS-COCO dataset. The configurations of this model are in the ```CocoConfig``` class in ```coco.py```.
# 
# For inferencing, modify the configurations a bit to fit the task. To do so, sub-class the ```CocoConfig``` class and override the attributes you need to change.

# In[3]:


class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    IMAGE_MAX_DIM=512
    IMAGE_MIN_DIM=512
    IMAGE_SHAPE=[512,512,3]
    NUM_CLASSES=2

config = InferenceConfig()
config.display()


# ## Create Model and Load Trained Weights

# In[4]:


# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)


# ## Class Names
# 
# The model classifies objects and returns class IDs, which are integer value that identify each class. Some datasets assign integer values to their classes and some don't. For example, in the MS-COCO dataset, the 'person' class is 1 and 'teddy bear' is 88. The IDs are often sequential, but not always. The COCO dataset, for example, has classes associated with class IDs 70 and 72, but not 71.
# 
# To improve consistency, and to support training on data from multiple sources at the same time, our ```Dataset``` class assigns it's own sequential integer IDs to each class. For example, if you load the COCO dataset using our ```Dataset``` class, the 'person' class would get class ID = 1 (just like COCO) and the 'teddy bear' class is 78 (different from COCO). Keep that in mind when mapping class IDs to class names.
# 
# To get the list of class names, you'd load the dataset and then use the ```class_names``` property like this.
# ```
# # Load COCO dataset
# dataset = coco.CocoDataset()
# dataset.load_coco(COCO_DIR, "train")
# dataset.prepare()
# 
# # Print class names
# print(dataset.class_names)
# ```
# 
# We don't want to require you to download the COCO dataset just to run this demo, so we're including the list of class names below. The index of the class name in the list represent its ID (first class is 0, second is 1, third is 2, ...etc.)

# In[5]:


# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
class_names = ['BG', 'cell']



# ## Run Object Detection

# In[ ]:
#for k in range(10):
    # Load a random image from the images folder
file_names = next(os.walk(IMAGE_DIR))[2]
image = skimage.io.imread(os.path.join(IMAGE_DIR, random.choice(file_names)))

    # Run detection
#results = model.detect([image], verbose=1)

    # Visualize results
#r = results[0]
#visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
#                                class_names, r['scores'])fraadjust_gammame


# In[ ]:
def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)

def detect(frame):
    #(H,W)=frame.shape[:2]
    #ROI_MASK=np.zeros((H,W))
    #ROI_MASK[:int(H*0.3),:]=1
    #frame_cropped=cv2.bitwise_and(frame, frame, mask=ROI_MASK.astype(np.uint8))
    #frame_cropped_resized=cv2.resize(frame_cropped,(800,600))
    #cv2.imshow("Mask",frame_cropped_resized)
    #results = model.detect([frame_cropped])
    
    #kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    #img = cv2.filter2D(frame, -1, kernel)
    img=adjust_gamma(frame,0.4)
    results = model.detect([img])
    img=cv2.resize(img,(800,600))
    cv2.imshow("Mask",img)
    r=results[0]
    return  r['rois'], r['masks'], r['scores']







# In[ ]:





# In[ ]:




