"""
The constants of coordinates have the 
following order,taking in consideration the
organs:

----------
 A1 | A2 |
---------|
 B1 | B2 |
---------|
 C1 | C2 |
---------|
  | D |
  
A1 = Liver
A2 = Spleen
B1 = Rkidney
B2 = Lkidney
C1 = Rureter
C2 = Lureter
D = Bladder
"""
from imutils import resize
from cv2 import imread


def read_resize(filename):
    """
    Reads a file and resizes the image to
    a height of 500
    """
    HEIGHT = 500
    img = imread(filename)
    resized_img = resize(img, height = HEIGHT)

    return resized_img


def img_fraction(image, h_w : str, fraction : int) -> int:
    """
    Returns the size of a certain dimension of an image
    ('h' for height or 'w' for width) divided by the
    fraction parameter
    """
    if h_w == 'h':
        i = 0
    elif h_w ==  'w':
        i = 1
    else:
        raise ValueError("Only 'h' and 'w' are valid values")
    
    img_dimension = (image.shape)[i]

    return int(img_dimension/fraction)


def img_A1(image):
    """A1"""
    a1_y = img_fraction(image, 'h', 2)
    
    a1_y = a1_y + int(a1_y/7)
    a1_x = img_fraction(image, 'w', 2)
    
    return image[:a1_y, :a1_x]


def img_A2(image):
    """A2"""
    a1_y = img_fraction(image, 'h', 2.5)
    a1_x = img_fraction(image, 'w', 3)
    return image[:a1_y, a1_x:]


def img_B1(image):
    """B1"""
    start_y = img_fraction(image, 'h', 4)
    end_y = img_fraction(image, 'h', 1.5)
    
    b1_x = img_fraction(image, 'h', 2.5)
    b1_y= range(start_y, end_y)
    
    return image[b1_y, :b1_x]


def img_B2(image):
    """B2"""
    start_y = img_fraction(image, 'h', 5)
    end_y = img_fraction(image, 'h', 1.5)
    
    b1_x = img_fraction(image, 'h', 3)
    b1_y = range(start_y, end_y)
    
    return image[b1_y, b1_x:]


def img_C1(image):
    """C1"""
    start_y = img_fraction(image, 'h', 4)
    end_y = int(start_y * 3.2)

    end_x = img_fraction(image, 'w', 2)
    start_x = int(end_x/2.5)

    return image[start_y: end_y, start_x:end_x]


def img_C2(image):
    """C2"""
    start_y = img_fraction(image, 'h', 4)
    end_y = int(start_y * 3.2)

    start_x = img_fraction(image, 'w', 2.3)
    end_x = int(start_x + start_x/1.5)

    return image[start_y: end_y, start_x:end_x]


def img_D(image):
    """D"""
    start_y = img_fraction(image, 'h', 5) * 3
    end_y = img_fraction(image, 'h', 8) * 7

    start_x = img_fraction(image, 'w', 5)
    end_x = start_x * 4
    
    return image[start_y:end_y, start_x:end_x]