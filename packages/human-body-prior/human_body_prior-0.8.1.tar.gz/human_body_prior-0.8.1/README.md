# VPoser: Variational Human Pose Prior
![alt text](github_data/vposer_samples.png "Interpolation of novel poses on the smoother VPoser latent space.")

## Description
Human joint configuration, also called as pose, is restricted by biomechanics of our body. 
Utilizing these constrains accuratly would be a corner stone of many computer vision tasks, 
such as estimating 3D human body parameters from 2D keypoints, detecting anomolies, and etc.

Here we present a method that is used in [SMPLify-X](https://smpl-x.is.tue.mpg.de/). 
Our variational human pose prior, named as VPoser, has the following features: 
 - is end-to-end differentiable
 - provides a way to penalizes impossible poses while allowing possible ones
 - effectively considers interdependency of configurations of the joints
 - intorduces a more efficient, and lower dimensional representation for human pose
 - can be used as a generative source for data dependent tasks
    

## Table of Contents
  * [Description](#description)
  * [Installation](#installation)
  * [Loading trained models](#Loading trained models) 
  * [Example](#example)
  * [Citation](#citation)
  * [Contact](#contact)
  * [License](#license)

![alt text](github_data/latent_interpolation_1.gif "Interpolation of novel poses on the smoother VPoser latent space.")
![alt text](github_data/latent_interpolation_2.gif "Interpolation of novel poses on the smoother VPoser latent space.")
![alt text](github_data/latent_interpolation_3.gif "Interpolation of novel poses on the smoother VPoser latent space.")


## Installation

To install the model simply you can:
1. To install from PyPi simply run: 
  ```bash
  pip install human_body_prior
  ```
2. Clone this repository and install it using the *setup.py* script: 
```bash
git clone https://github.com/nghorbani/human_body_prior
python setup.py install
```

## Loading Trained Models

To download the *VPoser* trained models go to the [project website](https://smpl-x.is.tue.mpg.de/) and register to get access to the downloads section. Afterwards, you can follow [model loading tutorial](human_body_prior/tutorials/README.md) to load and use your trained models.

## Train VPoser
We train VPoser, using a [variational autoencoder](https://arxiv.org/abs/1312.6114), 
which learns a latent representation of human pose and regularizes the distribution of the latent code to be a normal distribution.
We train our prior on the data released by [AMASS](https://amass.is.tue.mpg.de/), 
namely SMPL pose parameters of various publicly available human motion capture datasets. 
You can follow [data preparation tutorial](human_body_prior/data/README.md) to learn how to download and prepare AMASS for VPoser.
Afterwards, you can [Train VPoser from scratch](human_body_prior/train/README.md). 

## Tutorials
* [VPoser pose space for SMPL body model](human_body_prior/body_model/README.md)
* [Sampling novel poses from VPoser](human_body_prior/tutorials/README.md)
* [Preparing the training dataset](human_body_prior/data/README.md)
* [Train VPoser from scratch](human_body_prior/train/README.md)

## License

Software Copyright License for **non-commercial scientific research purposes**.
Please read carefully the [terms and conditions](https://github.com/vchoutas/smplx/blob/master/LICENSE) and any accompanying documentation before you download and/or use the SMPL-X/SMPLify-X model, data and software, (the "Model & Software"), including 3D meshes, blend weights, blend shapes, textures, software, scripts, and animations. By downloading and/or using the Model & Software (including downloading, cloning, installing, and any other use of this github repository), you acknowledge that you have read these terms and conditions, understand them, and agree to be bound by them. If you do not agree with these terms and conditions, you must not download and/or use the Model & Software. Any infringement of the terms of this agreement will automatically terminate your rights under this [License](./LICENSE).
