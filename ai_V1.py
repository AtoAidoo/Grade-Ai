import os
import cv2
import numpy as np

# For image enhancement
from skimage import exposure, restoration
from skimage.color import rgb2gray

# For perspective distortion
import imgaug as ia
from imgaug import augmenters as iaa

# For light variation
import random

def retrieve_and_preprocess_image(filename):
    """Retrieves an image from the temp storage and preprocesses it.

    Args:
        filename (str): The name of the image file.

    Returns:
        numpy.ndarray: The preprocessed image.
    """

    image_path = os.path.join(TEMP_DIR, filename)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB for OpenCV

    # Preprocessing steps (optional, adjust as needed)
    # image = cv2.resize(image, (desired_width, desired_height))
    # image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigmaX=0, sigmaY=0)

    return image

def enhance_image(image):
    """Enhances the image using various techniques.

    Args:
        image (numpy.ndarray): The input image.

    Returns:
        numpy.ndarray: The enhanced image.
    """

    # Contrast stretching
    p2, p98 = np.percentile(image, (2, 98))
    img_rescale = exposure.rescale_intensity(image, in_range=(p2, p98))

    # Denoising (optional)
    # img_denoised = restoration.denoise_tv_chambolle(img_rescale, weight=0.1)

    return img_rescale

def distort_perspective(image):
    """Applies perspective distortion to the image.

    Args:
        image (numpy.ndarray): The input image.

    Returns:
        numpy.ndarray: The distorted image.
    """

    seq = iaa.Sequential([
        iaa.PerspectiveTransform(scale=(0.01, 0.1))
    ])

    return seq.augment_image(image)

def vary_light(image):
    """Adjusts the image's lighting conditions.

    Args:
        image (numpy.ndarray): The input image.

    Returns:
        numpy.ndarray: The image with varied lighting.
    """

    # Randomly adjust brightness and contrast
    brightness = random.uniform(-0.5, 0.5)
    contrast = random.uniform(0.8, 1.2)

    adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

    return adjusted

def process_image(filename):
    image = retrieve_and_preprocess_image(filename)
    enhanced_image = enhance_image(image)
    distorted_image = distort_perspective(enhanced_image)
    final_image = vary_light(distorted_image)

    # Save or display the final image as needed
    cv2.imwrite("output.jpg", final_image)

    return final_image