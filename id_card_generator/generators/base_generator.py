from pathlib import Path
import csv
import datetime
import string
import random
from PIL import Image, ImageDraw, ImageFont

from id_card_generator.utils.constans import IMG_EXTENSION
from id_card_generator.utils.utils import load_files_with_given_extension


class BaseGenerator:
    def __init__(self) -> None:
        super().__init__()
        self.data_path = Path("data")
        self.face_data_path = self.data_path.joinpath("faces")
        self.face_images_paths = load_files_with_given_extension(
            self.face_data_path, ext=[IMG_EXTENSION]
        )
