# GCC support can be specified at major, minor, or micro version
# (e.g. 8, 8.2 or 8.2.0).
# See https://hub.docker.com/r/library/gcc/ for all supported GCC
# tags from Docker Hub.
# See https://docs.docker.com/samples/library/gcc/ for more on how to use this image
#FROM gcc:latest
FROM ubuntu:20.04
FROM tensorflow/tensorflow:latest-gpu-jupyter
FROM tensorflow_jupyterlab_v5:custom_image_yolov5
WORKDIR /app
# These commands copy your files into the specified directory in the image
# and set that as the working location

COPY . ~/tensorflow/tensorflow_deeplearning/

RUN echo "********/home/eurolink/tensorflow_deeplearning*************BUILDING********************"
# This command compiles your app using GCC, adjust for your source code


# This command runs your application, comment out this line to compile only
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

#LABEL Name=tensorflowtensorrt Version=0.0.1
