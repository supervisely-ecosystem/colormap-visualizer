from supervisely.app.widgets import Container, Switch, Field, Select
from supervisely.sly_logger import logger
import cv2

need_processing = Switch(switched=True, widget_id="need_processing_widget")
processing_field = Field(
    title="Apply colormap",
    description="If turned on, the effect will be aplied",
    content=need_processing,
    widget_id="processing_field_widget",
)

colormaps_cv2 = {
    "AUTUMN": cv2.COLORMAP_AUTUMN,
    "BONE": cv2.COLORMAP_BONE,
    "JET": cv2.COLORMAP_JET,
    "WINTER": cv2.COLORMAP_WINTER,
    "RAINBOW": cv2.COLORMAP_RAINBOW,
    "OCEAN": cv2.COLORMAP_OCEAN,
    "SUMMER": cv2.COLORMAP_SUMMER,
    "SPRING": cv2.COLORMAP_SPRING,
    "COOL": cv2.COLORMAP_COOL,
    "HSV": cv2.COLORMAP_HSV,
    "PINK": cv2.COLORMAP_PINK,
    "HOT": cv2.COLORMAP_HOT,
    "PARULA": cv2.COLORMAP_PARULA,
    "MAGMA": cv2.COLORMAP_MAGMA,
    "INFERNO": cv2.COLORMAP_INFERNO,
    "PLASMA": cv2.COLORMAP_PLASMA,
    "VIRIDIS": cv2.COLORMAP_VIRIDIS,
    "CIVIDIS": cv2.COLORMAP_CIVIDIS,
    "TWILIGHT": cv2.COLORMAP_TWILIGHT,
    "TWILIGHT_SHIFTED": cv2.COLORMAP_TWILIGHT_SHIFTED,
    "TURBO": cv2.COLORMAP_TURBO,
    "DEEPGREEN": cv2.COLORMAP_DEEPGREEN,
}
colormaps = list(colormaps_cv2.values())
items = [Select.Item(i, name.title()) for i, name in enumerate(colormaps_cv2)]
colormap_select = Select(items, widget_id="colormap_select_widget")
colormap_field = Field(
    title="Colormap",
    description="Select the colormap to apply",
    content=colormap_select,
    widget_id="colormap_field_widget",
)

layout = Container(widgets=[processing_field, colormap_field], widget_id="layout_widget")

@need_processing.value_changed
def processing_switched(is_switched):
    logger.debug(f"Processing is now {is_switched}")
    if is_switched:
        colormap_select.enable()
    else:
        colormap_select.disable()
