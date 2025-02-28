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
    img_data = getattr(app.state, "imagePixelsData", app.get_current_image())
    new_img = process_img(img_data, colormap)
    app.replace_current_image(new_img)


@app.run_function
def main():
    if hasattr(app.state, "imagePixelsData") is False:
        setattr(app.state, "imagePixelsData", None)
    if hasattr(app.state, "imagePixelsDataImageId") is False:
        setattr(app.state, "imagePixelsDataImageId", 0)

    if app.state.imagePixelsDataImageId != app._context.imageId:
        app.state.imagePixelsData = app.get_current_image()
        app.state.imagePixelsDataImageId = app._context.imageId
        if not need_processing.is_on():
            app.replace_current_image(app.state.imagePixelsData)
            return
        colormap = colormaps[colormap_select.get_value()]
        new_img = process_img(app.state.imagePixelsData, colormap)
        app.replace_current_image(new_img)
