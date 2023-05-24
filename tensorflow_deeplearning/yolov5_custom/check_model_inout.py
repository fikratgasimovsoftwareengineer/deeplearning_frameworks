import tensorrt as trt

def load_engine(engine_file_path):
    TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
    runtime = trt.Runtime(TRT_LOGGER)
    
    with open(engine_file_path, 'rb') as f:
        engine = runtime.deserialize_cuda_engine(f.read())
        
    return engine

engine_file_path = '/deeplearning/YOLOV5_TRASH/yolov5/runs/train/exp4/weights/yolov5s.engine'

engine = load_engine(engine_file_path)


# get input
input_tensor_name = engine.get_binding_name(0)
output_tensor_name = engine.get_binding_name(1)

# get input output tensor shapes

input_shape = engine.get_binding_shape(0)
output_shape = engine.get_binding_shape(1)

print(f'Input tensor name : {input_tensor_name}, shape: {input_shape}')
print(f'Output tensor name : {output_tensor_name}, shape: {output_shape}')