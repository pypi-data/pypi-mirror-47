import cv2
import os
import numpy as np

from microlab.io.files import delete_file

def timelapse(table):
    t = []
    for i in range(len(table)):
        t.append(float(i))
    return t


# Show
def show_image(title, image):
    print(title, image, end='.....')


def show_mask(mask):
    cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
    cv2.imshow("Mask", mask)
    cv2.waitKey(0)


# Convert
def convert_to_gray(image):
    print(' Converting to gray ', image)


def create_mask(width, height, verbose=False):
    size = (height, width)
    mask = np.zeros(size, dtype="uint8")
    if verbose:
        print('[ mask    ] created with shape {}'.format(mask.shape))
    return mask


def export_mask(mask, file_name, verbose=False):
    cv2.imwrite(file_name, mask)
    if verbose:
        print('[ mask    ]  exported to {}'.format(file_name))


def draw_phase_on_mask(mask, phase, verbose=False):
    # dimensions of the mask
    height, width = mask.shape

    # start marker from left middle node
    marker_point = (int(0), int(height/2))

    if verbose:
        print('--> Drawing {} points on mask '.format(len(phase)))

    for x, y in zip(timelapse(phase[0]), phase[1]):
        # Mathematics world
        # |
        # |
        # V
        # Computer world
        pixel = (marker_point[0] + int(x), marker_point[1] - int(y))

        # Draw the pixel on mask
        cv2.circle(img=mask, center=pixel, radius=1, color=(255, 255, 255), thickness=0)

    return mask


# Representation
def create_representation(phase1, phase2, width, height, verbose=False):
    center = (int(width/2), int(height/2))

    # create representation mask
    mask = create_mask(width=width, height=height, verbose=verbose)

    # draw the center of the mask
    cv2.circle(img=mask, center=center, radius=0, color=(255, 255, 255), thickness=5)

    # draw phase 1
    mask = draw_phase_on_mask(mask, phase=phase1, verbose=verbose)

    # draw phase 2
    mask = draw_phase_on_mask(mask, phase=phase2, verbose=verbose)

    return mask
