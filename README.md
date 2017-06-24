# CV_backend
Machine Learning backend to detect fake images

- [x] Setup Azure instance with GPU (N6)
- [x] Install NVIDIA driver and CUDA
- [ ] Build OpenCV3
- [ ] Install Deep Learning libraries (Chainer, Darknet, Tensorflow)
- [ ] Build Google reverse search hack
- [ ] Build ELA algorithm with OpenCV
- [ ] Implement ELA image fakeness scoring
- [ ] Use Darknet for object detection
- [ ] Use Chainer for caption generation
- [ ] Train neural network to recognize weather, number plate, buildings, signs
- [ ] Compare analysis results with original Tweet data
- [ ] Return JSON report data

# NVIDIA CUDA 8.0 for Ubuntu 16.04
https://developer.nvidia.com/compute/cuda/8.0/Prod2/local_installers/cuda_8.0.61_375.26_linux-run

# CUDNN 5.1
https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v5.1/prod_20161129/8.0/cudnn-8.0-linux-x64-v5.1-tgz

# Env variable
Add to `.bashrc`:
```
#Define CUDA_HOME environment variable
export CUDA_HOME=/usr/local/cuda-8.0
#Define LD_LIBRARY_PATH environment variable
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64
#Add CUDA_HOME to PATH
export PATH=${CUDA_HOME}/bin:${PATH}
```

# OpenCV
https://gist.github.com/filitchp/5645d5eebfefe374218fa2cbf89189aa

# Useful Tools:
tmux, htop, gpustat
