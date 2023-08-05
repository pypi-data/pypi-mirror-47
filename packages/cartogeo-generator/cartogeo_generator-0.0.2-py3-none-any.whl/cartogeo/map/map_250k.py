import numpy as np
from typing import Tuple, List
from .map_25_or_50k import Map
from ..coord import Coord


class Map250k(Map):
    prefix: str                 # The prefix to the specific map data folder from the generic data folder
    box_mm: int = 40            # Width/Height of a box on the map (in millimeters)
    box_pixels: int = 400       # Width/Height of a box on the map (in pixels)
    scale: str = "1:250000"     # The name of the scale as a string
    scale_unit: int = 8         # PDF visual scale unit size

    # PDF visual scale 11 labels
    scale_labels: List[str] = ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20 km"]

    # The size of the map on the PDF in boxes
    pdf_size_landscape: Tuple[float, float] = (7, 4)
    pdf_size_portrait: Tuple[float, float] = (4.75, 6)
    pdf_size_scale: int = 10    # Increase in 1 X/Y equal to increase in (1*pdf_size_scale) boxes

    def __init__(self):
        self.prefix = Map.map_data_path() + "raster-250k/"

    def build_sources(self, coord1: Coord, coord2: Coord) -> list:
        """
        Builds a 2D array of source images that should be used to construct the map
        :param coord1: Top left coord
        :param coord2: Bottom right coord
        :return: A 2D array of source images
        """
        output = []
        for y in range(coord1.sheet_tuple[1], coord2.sheet_tuple[1] + 1):
            row = []
            for x in range(coord1.sheet_tuple[0], coord2.sheet_tuple[0] + 1):
                row.append(Coord.tuple_to_sheet((x, y)).lower() + ".tif")
            output.append(row)
        return output

    def calculate_crop(self, coord1: Coord, coord2: Coord) -> Tuple[float, float, float, float]:
        left = coord1.x / 10
        top = 10 - (coord1.y / 10)
        right = 10 - (coord2.x / 10)
        bottom = coord2.y / 10
        return left, top, right, bottom

    def crop(self, structure: np.array, coord1: Coord, coord2: Coord) -> np.array:
        """
        Crop the structure which contains all of the source imagery to only contain the requested area
        :param structure: Uncropped numpy image structure
        :param coord1: Top left coord
        :param coord2: Bottom right coord
        :return: Cropped numpy image structure
        """
        left, top, right, bottom = self.calculate_crop(coord1, coord2)
        return self._crop_boxes(structure, left, top, right, bottom)
