import cv2
import numpy as np
from sly_sdk.webpy import WebPyApplication
from src.gui import layout, need_processing, colormap_select, colormaps

app = WebPyApplication(layout)
colormap = colormaps[colormap_select.get_value()]

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


@app.run_function
def main():
    global colormap
    if hasattr(app.state, "imagePixelsData") is False:
        setattr(app.state, "imagePixelsData", app.get_current_image())
    if hasattr(app.state, "imagePixelsDataImageId") is False:
        setattr(app.state, "imagePixelsDataImageId", app.get_current_image_id())
    if not need_processing.is_on():
        app.replace_current_image(app.state.imagePixelsData)
        return

    if app.state.imagePixelsDataImageId != app.get_current_image_id():
        app.state.imagePixelsData = app.get_current_image()
        app.state.imagePixelsDataImageId = app.get_current_image_id()
    new_img = process_img(app.state.imagePixelsData, colormap)
    app.replace_current_image(new_img)
