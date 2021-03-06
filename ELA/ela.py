#!/usr/bin/env python

from PIL import Image, ImageChops
import cv2
import numpy as np

base = '/home/mehdi/work/CV_backend/'

# ORIG = '../fake_ipad.jpg'
# TEMP = 'temp.jpg'
# SCALE = 10
#
#
# def ELA():
#     original = Image.open(ORIG)
#     original.save(TEMP, quality=90)
#     temporary = Image.open(TEMP)
#
#     diff = ImageChops.difference(original, temporary)
#     d = diff.load()
#     WIDTH, HEIGHT = diff.size
#     for x in range(WIDTH):
#         for y in range(HEIGHT):
#             d[x, y] = tuple(k * SCALE for k in d[x, y])
#
#     diff.show()

def cv2_ELA(name):
    input_image = cv2.imread(name)

    scale = 15
    quality = 75

    cv2.imwrite(base+'ELA/temp.jpg', input_image, [cv2.IMWRITE_JPEG_QUALITY, quality])

    compressed_image = cv2.imread(base+'ELA/temp.jpg')

    output_image = (input_image - compressed_image) * scale

    gray_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2GRAY)

    nonzero = cv2.countNonZero(gray_image)
    total = output_image.shape[0] * output_image.shape[1]
    zero = total - nonzero
    ratio = zero * 100 / float(total)

    cv2.imwrite(base+'ELA/results/{}_results.png'.format(name), output_image)
    return ratio, output_image

if __name__ == '__main__':
    #ELA()
    for name in ['lion', 'real_ipad', 'fake_ipad']:
        ratio, output_image = cv2_ELA('../example_images/{}.jpg'.format(name))
        print name
        print "# Image shape:", output_image.shape
        print "# Average pixel:", np.mean(output_image)
        print "# Black pixel ratio:", ratio
