import os

class TRTInference:
        
    # specify engine file path and input and output shape
    def __init__(self, class_labels_file):
  
        self.class_labels_file =  class_labels_file
            
        with open(self.class_labels_file, 'r') as class_read:
            self.class_labels = [line.strip() for line in class_read.readlines()]
            
            print(self.class_labels)
path_to_class = "/deeplearning/resnet/imagenet_classes.txt"
inference = TRTInference(path_to_class)