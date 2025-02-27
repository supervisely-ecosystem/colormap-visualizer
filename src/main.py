import cv2
import numpy as np
from sly_sdk.webpy import WebPyApplication
from src.gui import layout, need_processing, colormap_select, colormaps

app = WebPyApplication(layout)

def process_img(img, colormap):
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    new_img = cv2.applyColorMap(img_bgr, colormap)
    new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
    alpha_channel = img[:, :, 3]
    return np.dstack((new_img, alpha_channel))


@colormap_select.value_changed
def colormap_changed(value):
    colormap = colormaps[value]
    img = app.get_current_image()
    new_img = process_img(img, colormap)
    app.replace_current_image(new_img)


@app.event(app.Event.ManualSelected.ImageChanged)
def image_changed(event: WebPyApplication.Event.ManualSelected.ImageChanged):
    print("Image changed: ", app._context.imageId)
    if not need_processing.is_on():
        return
    colormap = colormaps[colormap_select.get_value()]
    img = app.get_current_image()
    new_img = process_img(img, colormap)
    app.replace_current_image(new_img)
