import cv2
import numpy as np
from sly_sdk.webpy import WebPyApplication
from src.gui import layout, need_processing, colormap_select, colormaps

app = WebPyApplication(layout)

def process_img(img, colormap):
    return np.array(cv2.applyColorMap(img, colormap))


@colormap_select.value_changed
def colormap_changed(value):
    colormap = colormaps[value]
    img = app.get_current_image()
    new_img = process_img(img, colormap)
    app.replace_current_image(new_img)


@app.event(app.Event.ManualSelected.ImageChanged)
def image_changed(event: WebPyApplication.Event.ManualSelected.ImageChanged):
    if not need_processing.is_on():
        return
    colormap = colormaps[colormap_select.get_value()]
    img = app.get_current_image()
    new_img = process_img(img, colormap)
    app.replace_current_image(new_img)
