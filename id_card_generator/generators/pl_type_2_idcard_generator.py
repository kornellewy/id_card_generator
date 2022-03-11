from pathlib import Path
import csv
import datetime
import string
import random
from PIL import Image, ImageDraw, ImageFont

from utils.utils.constants import IMG_EXTENSION

from id_card_generator.generators.base_generator import BaseGenerator


class PLType2IdcardGenerator(BaseGenerator):
    def __init__(self) -> None:
        super().__init__()

        self.bbox_front_img_big = [50, 300, 500, 875]
        self.bbox_front_img_big_size = (
            self.bbox_front_img_big[2] - self.bbox_front_img_big[0],
            self.bbox_front_img_big[3] - self.bbox_front_img_big[1],
        )
        self.bbox_front_img_small = [1250, 655, 1430, 870]
        self.bbox_front_img_small_size = (
            self.bbox_front_img_small[2] - self.bbox_front_img_small[0],
            self.bbox_front_img_small[3] - self.bbox_front_img_small[1],
        )
        self.bbox_back_img = [845, 180, 970, 345]
        self.bbox_back_img_size = (
            self.bbox_back_img[2] - self.bbox_back_img[0],
            self.bbox_back_img[3] - self.bbox_back_img[1],
        )
        self.bbox_surname = (593, 310)
        self.bbox_first_name = (593, 455)
        self.bbox_family_name = (593, 580)
        self.bbox_parents_names = (593, 715)
        self.bbox_date_of_birth = (593, 850)
        self.bbox_sex = (1070, 850)
        self.bbox_pesel = (205, 60)
        self.bbox_nationality = (205, 150)
        self.bbox_place_of_birth = (40, 225)
        self.bbox_issuing_authority = (40, 300)
        self.bbox_id_card_number = (720, 100)
        self.bbox_date_of_issue = (670, 222)
        self.bbox_expiry_date = (670, 300)
