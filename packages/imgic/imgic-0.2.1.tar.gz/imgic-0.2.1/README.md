## imgic v0.1

imgic is a Python module that contains basic tools for image augmentation. The
current version of the module takes numpy ndarrays as inputs and supports the 
following methods:

- Crop (fixed size, relative crop, random crop)
- Resize (fixed/relative)
- Flip (horizontal/vertical)
- Dropout (random)
- Combine (2 images with selected opacity)
- Blur (Gaussian with selected strength - SLOW!)
- Color jitter
- Channel shuffle

The module supports method chaining and outputs numpy ndarrays.

# Example syntax

> import imageio
> import matplotlib.pyplot as plt
> img = imageio.imread("https://image.shutterstock.com/image-photo/feral-cat-outback-australia-450w-685502620.jpg")
> plt.imshow(img)
> plt.show()

![alt text](https://image.shutterstock.com/image-photo/feral-cat-outback-australia-450w-685502620.jpg)

> import imgic
> test_img = imgio.Img(img)
> test_img = test_img.resize(height = 200, width = 200).blur().flip(axis=0)

> print(test_img)
>> Output: Image of 200x200

> plt.imshow(test_img.image)
>> Output: 
![alt text](https://i.ibb.co/KF53Jrw/Figure-1.png)


