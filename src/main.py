import cv2
import numpy as np
from sly_sdk.webpy import WebPyApplication
from src.gui import layout, need_processing, colormap_select, colormaps

app = WebPyApplication(layout)

original_img_data = None

def process_img(img, colormap):
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    new_img = cv2.applyColorMap(img_bgr, colormap)
    new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
    alpha_channel = img[:, :, 3]
    return np.dstack((new_img, alpha_channel))


@colormap_select.value_changed
def colormap_changed(value):
    global original_img_data
    colormap = colormaps[value]
    if original_img_data is None:
        img = app.get_current_image()
        original_img_data = img
    img = original_img_data
    new_img = process_img(img, colormap)
    app.replace_current_image(new_img)


@app.event(app.Event.ImageChanged)
def image_changed(event: WebPyApplication.Event.ImageChanged):
    global original_img_data
    original_img_data = app.get_current_image()
    app._context.imageId = event.image_id
    if not need_processing.is_on():
        return
    colormap_changed(colormap_select.get_value())
