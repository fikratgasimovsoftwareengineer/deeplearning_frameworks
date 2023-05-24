import os
from PIL import Image

image_path = '/deeplearning/resnet/images'

count = 0
for img in os.listdir(image_path):
    
    if img.endswith('.jpg') or img.endswith('.png') or img.endswith('jpeg'):
        count +=1
        img_org = os.path.join(image_path, img)
        
        img = Image.open(img_org)
       # print(img_org)
        
        width, height = img.size
        print(width, height)
        print('Number of image', count)
       