# Gogh Get Paper (WebGAN)

We explore generating high resolution images by progressively generating 64x64 images using a Deep Convolutional Generative Adversarial Network (DCGAN) and Convolutional Neural Networks (CNNs).

### Data Collection

Retrieving images from Reddit/EarthPorn (PHOTOS): `crawlers/notebooks/Reddit Crawler.ipynb`

Splitting images into 64x64 snapshots (IMAGESPLIT): `data/Crop Images to Smaller Size.ipynb`

Creating 2 by 2 sub-images (EXTENSIONSPLIT): `data/Create Extend Training Data.ipynb`

### Model Training

RootGAN: `data/Base GAN.ipynb`

RightExtender: `data/Extend NN.ipynb`

DownExtender: `data/Extend NN Down.ipynb`

DiagonalExtender: `data/Extend NN Diagonal.ipynb`
