import cv2
import numpy as np
import random

def pixels(photo: str, p_1, p_2):
    input = cv2.imread(photo)
    height, width = input.shape[:2]
    w, h = (p_1,p_2)
    temp = cv2.resize(input, (w, h), interpolation=cv2.INTER_LINEAR)
    output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
    image_output_name = f'output{random.randint(1,5000)}.jpg'
    cv2.imwrite(image_output_name, output)
    return image_output_name
def bilateralFilter(photo: str, diametr, sgmaColor, sgmaSpace):
    import cv2 
    img = cv2.imread((photo),1)
    kernel = np.ones((5,5),np.float32)/25 
    blur = cv2.bilateralFilter(img,diametr,sgmaColor,sgmaSpace) 
    image_output_name = f'output{random.randint(1,5000)}.jpg'
    cv2.imwrite(image_output_name, blur)
    return image_output_name

def black_and_white(photo:str):
    image = cv2.imread(photo, cv2.IMREAD_GRAYSCALE)
    image_output_name = f'output{random.randint(1,5000)}.jpg'
    cv2.imwrite(image_output_name, image)
    return image_output_name
def image_sharpness(photo: str):
    input = cv2.imread(photo)
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    image = cv2.filter2D(input, -1, kernel)
    image_output_name = f'output{random.randint(1,5000)}.jpg'
    cv2.imwrite(image_output_name, image)
    return image_output_name
