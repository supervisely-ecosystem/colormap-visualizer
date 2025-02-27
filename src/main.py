import cv2
import numpy as np
from sly_sdk.webpy import WebPyApplication
from sly_sdk.sly_logger import logger

from src.gui import layout, need_processing, colormap_select


app = WebPyApplication(layout)

def process_img(img, colormap):
    return np.array(cv2.applyColorMap(img, colormap))

def main():
    if not need_processing.is_on():
        return
    curr_img = app.get_current_image()
    colormap = colormap_select.get_value()
    return process_img(curr_img, colormap)