import tkinter
from PIL import Image
import os
from typing import List, Tuple


class ExportData:
    _exportPath: str = ""
    _image_size: Tuple[int, int] = (2048, 2048)
    _max_dimension: int = 1024

    def load_export_path(self):
        tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
        self._exportPath = tkinter.filedialog.askdirectory()

    def calculate_atlas_count(self, directory: str) -> Tuple[int, List[str], List[str]]:
        total_image_size: int = 0
        png_files: List[str] = []
        oversized_files: List[str] = []
        max_dimension_files: List[str] = []

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".png"):
                    png_files.append(os.path.join(root, file))

        for png_file in png_files:
            image: Image.Image = Image.open(png_file)
            width: int = image.size[0]
            height: int = image.size[1]
            trimmed_image: Image.Image = image.crop(image.getbbox())

            if width > self._image_size[0] or height > self._image_size[1]:
                oversized_files.append(png_file)

            if width > self._max_dimension or height > self._max_dimension:
                max_dimension_files.append(png_file)

            mode: str = image.mode
            bits_per_channel: int = {
                "1": 1,
                "L": 8,
                "P": 8,
                "RGB": 24,
                "RGBA": 32,
                "CMYK": 32,
                "YCbCr": 24,
                "I": 32,
                "F": 32,
            }.get(mode, 0)
            channels: int = len(mode)
            pixel_size: int = bits_per_channel * channels // 8
            trimmed_image_size: int = (
                trimmed_image.size[0] * trimmed_image.size[1] * pixel_size
            )

            total_image_size += trimmed_image_size

        atlas_space: int = self._image_size[0] * self._image_size[1] * pixel_size
        atlas_count: int = (
            total_image_size + atlas_space - 1
        ) // atlas_space  # Round up the division

        return atlas_count, oversized_files, max_dimension_files
