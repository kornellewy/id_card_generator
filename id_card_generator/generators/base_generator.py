from pathlib import Path
import csv
import datetime
import string
import random
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as ImageType
from typing import Tuple

from id_card_generator.utils.constans import IMG_EXTENSION
from id_card_generator.utils.utils import load_files_with_given_extension


class BaseGenerator:
    def __init__(self) -> None:
        super().__init__()
        self.data_path = Path("data")
        self.face_data_path = self.data_path.joinpath("faces")
        self.female_face_data_path = self.face_data_path.joinpath("female")
        self.female_face_images_paths = load_files_with_given_extension(
            self.female_face_data_path, ext=[IMG_EXTENSION]
        )
        
        self.male_face_data_path = self.face_data_path.joinpath("male")
        self.male_face_images_paths = load_files_with_given_extension(
            self.male_face_data_path, ext=[IMG_EXTENSION]
        )
        
        self.id_templates_path = Path("data/id_template")

    def get_random_face(self, is_male: bool) -> Tuple[ImageType, ImageType]:
        if is_male:
            face_img_path = random.choice(self.male_face_images_paths)
        else:
            face_img_path = random.choice(self.female_face_images_paths)
        face_img = Image.open(face_img_path)
        face_img_gray = face_img.convert("LA")
        return face_img, face_img_gray

    # def get_
