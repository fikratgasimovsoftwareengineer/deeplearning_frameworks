import tensorrt as trt
import pycuda.autoinit
import pycuda.driver as cuda
import cv2
import numpy as np
import os
from PIL import Image
import yaml
import matplotlib.pyplot as plt

class TRTInference:
        
        
    # specify engine file path and input and output shape
    def __init__(self, engine_file_path, input_shape, output_shape, class_labels_file):
        self.logger = trt.Logger(trt.Logger.WARNING)

        ## load engine here
        self.engine = self.load_engine( engine_file_path)

        # craete context
        self.context = self.engine.create_execution_context()

        # input shape
        self.input_shape = input_shape
            
        # output shape
        self.output_shape = output_shape

        with open(class_labels_file) as class_read:
            self.class_labels = yaml.load(class_read, Loader=yaml.FullLoader)

    def load_engine(self, engine_file_path):
        with open(engine_file_path, 'rb') as f:
            runtime = trt.Runtime(self.logger)
            engine_desentriliazed = runtime.deserialize_cuda_engine(f.read())

            return engine_desentriliazed
            
    def preprocess_image(self, image_path):
        
        img = Image.open( image_path)
              
        # get image size
        width, height = img.size
        print(width, height)

        #img size = [224, 224]
        img = img.resize((self.input_shape[2], self.input_shape[3]), Image.NEAREST)

        img_np = np.array(img).astype(np.float32) / 255.0
            
        img_np = img_np.transpose((2,0,1))

        img_np = np.expand_dims(img_np, axis=0)
           

        return img_np
        
    def postprocess_img(self,outputs):
                
        #class_idx = outputs[0].argmax() 
        #
        #print("Class Detected: ", class_name)

       # return class_name
       
        class_probabilities = outputs[0, :, -6:]
        class_indices = np.argmax(class_probabilities, axis=-1)
    
        # Get the unique class indices
        unique_class_indices = np.unique(class_indices)

        # Map the class indices to class labels
        detected_classes = [self.class_labels[idx] for idx in unique_class_indices]

        print("Classes Detected: ", detected_classes)



    def inference_detection(self,image_path):

        inputs = self.preprocess_image(image_path)
            
        inputs = np.ascontiguousarray(inputs)

        outputs = np.empty(self.output_shape, dtype=np.float32)

        d_inputs = cuda.mem_alloc(1 * inputs.nbytes)

        d_outpus = cuda.mem_alloc(1 * outputs.nbytes)

        bindings = [d_inputs ,d_outpus]

        cuda.memcpy_htod(d_inputs, inputs)

        self.context.execute_v2(bindings)

            # copy output back to host
        cuda.memcpy_dtoh(outputs, d_outpus)

        result = self.postprocess_img(outputs)        

        d_inputs.free()

        d_outpus.free()

        self.display_recognized_image(image_path, result)

        return result   
        
    def display_recognized_image(self, image_path, class_label):
        
        image = Image.open(image_path)
            
        plt.imshow(image)
        plt.title(f'Recognized Image: {class_label}')
        plt.axis('off')
        path_to_detected_img = "/deeplearning/yolov5_custom/detected_images"
        if not os.path.exists(path_to_detected_img):
            os.makedirs(path_to_detected_img)
        save_img = os.path.join(path_to_detected_img, f'{class_label}.jpg')
        plt.savefig(save_img)
        plt.close()
        return save_img

engine_file_path ='/deeplearning/YOLOV5_TRASH/yolov5/runs/train/exp4/weights/yolov5s.engine'
# Load the TensorRT engine
input_shape = (1, 3, 640, 640)
output_shape = (1, 25200, 11)

image_path = '/deeplearning/yolov5_custom/images/metal79.jpg'

path_to_class = "/deeplearning/yolov5_custom/classes/classes.yaml"


inference = TRTInference(engine_file_path, input_shape, output_shape, path_to_class)

class_name = inference.inference_detection(image_path)
print(class_name)