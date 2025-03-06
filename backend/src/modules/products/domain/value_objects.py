from enum import Enum


class PartCategoryName(str, Enum):
    FRAME = "Frame"
    FRAME_FINISH = "Finish"
    WHEELS = "Wheels"
    RIM_COLOR = "Rim color"
    CHAIN = "Chain"
    STRING = "string"


class StockStatus(str, Enum):
    AVAILABLE = "available"
    OUT_OF_STOCK = "out_of_stock"
