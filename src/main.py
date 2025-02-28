import cv2
import numpy as np
from sly_sdk.webpy import WebPyApplication
from src.gui import layout, need_processing, colormap_select, colormaps

colormap = colormaps[colormap_select.get_value()]
apply_processing = need_processing.is_on()

app = WebPyApplication(layout)
state = app.state
if hasattr(state, "imagePixelsData") is False:
    setattr(state, "imagePixelsData", None)
if hasattr(state, "imagePixelsDataImageId") is False:
    setattr(state, "imagePixelsDataImageId", 0)

def process_img(img, colormap):
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    new_img = cv2.applyColorMap(img_bgr, colormap)
    new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
    alpha_channel = img[:, :, 3]
    return np.dstack((new_img, alpha_channel))


@colormap_select.value_changed
def colormap_changed(value):
    global colormap
    colormap = colormaps[value]
    new_img = process_img(state.imagePixelsData, colormap)
    app.replace_current_image(new_img)


@need_processing.value_changed
def processing_switched(is_switched):
    if is_switched is False:
        app.replace_current_image(app.get_current_image())
    global apply_processing
    apply_processing = is_switched


@app.run_function
def main():
    global colormap
    global apply_processing
    if apply_processing and state.imagePixelsDataImageId != app.get_current_image_id():
        state.imagePixelsData = app.get_current_image()
        state.imagePixelsDataImageId = app.get_current_image_id()
        new_img = process_img(state.imagePixelsData, colormap)
        app.replace_current_image(new_img)
