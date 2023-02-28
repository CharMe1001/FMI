# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cv2
from sympy import divisors
from numpy import intersect1d, random
from random import shuffle
from scipy.ndimage import rotate

photo = 'image.png'

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    img = cv2.imread(photo)

    N = len(img)
    M = len(img[0])

    scale = min(filter(lambda x: x > 20, intersect1d(divisors(N), divisors(M))))

    r1 = range(N // scale)
    r2 = range(M // scale)

    lst = [rotate(img[(x * scale):((x + 1) * scale), (y * scale):((y + 1) * scale)], angle=90 * random.randint(0, 4)) for x in r1 for y in r2]
    shuffle(lst)

    for i in range(N // scale):
        for j in range(M // scale):
            img[(i * scale):((i + 1) * scale), (j * scale):((j + 1) * scale)] = lst[i * (M // scale) + j]

    cv2.imshow('photo', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
