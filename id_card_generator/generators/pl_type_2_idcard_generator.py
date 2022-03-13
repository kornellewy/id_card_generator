from pathlib import Path
import csv
import datetime
import string
import random
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as ImageType
from typing import Tuple, Dict, Optional

from id_card_generator.utils.constans import IMG_EXTENSION
from id_card_generator.utils.utils import paste_img_with_blure
from id_card_generator.generators.base_generator import BaseGenerator


class PLType2IdcardGenerator(BaseGenerator):
    def __init__(self) -> None:
        super().__init__()
        self.id_template_front_path = self.id_templates_path.joinpath(
            "pl_type2_front.png"
        )
        self.id_template_back_path = self.id_templates_path.joinpath(
            "pl_type2_back.png"
        )

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
        self.bbox_back_end_code_line1 = (55, 420)
        self.bbox_back_end_code_line2 = (55, 470)
        self.bbox_back_end_code_line3 = (55, 520)

        self.male_name_first_csv_path = self.data_path.joinpath(
            "pl_names", "first_name", "lista_imion_męskich_os_żyjące_2020-01-21.csv"
        )
        self.male_name_second_csv_path = self.data_path.joinpath(
            "pl_names",
            "second_name",
            "lista_drugich_imion_męskich_os._żyjące_2020-01-21.csv",
        )
        self.male_surname_csv_path = self.data_path.joinpath(
            "pl_names",
            "surnames",
            "Wykaz_nazwisk_męskich_uwzgl_os__zmarłe_2020-01-22.csv",
        )
        self.female_name_first_csv_path = self.data_path.joinpath(
            "pl_names", "first_name", "lista_imion_żeńskich_os_żyjące_2020-01-21.csv"
        )
        self.female_name_second_csv_path = self.data_path.joinpath(
            "pl_names",
            "second_name",
            "lista_drugich_imion_żeńskich_os.żyjące_2020-01-21.csv",
        )
        self.female_surname_csv_path = self.data_path.joinpath(
            "pl_names",
            "surnames",
            "Wykaz_nazwisk_żeńskich_uwzgl_os__zmarłe_2020-01-22.csv",
        )

        self.male_names_first = self.load_data_from_csv(self.male_name_first_csv_path)
        self.male_names_second = self.load_data_from_csv(self.male_name_second_csv_path)
        self.male_surname = self.load_data_from_csv(self.male_surname_csv_path)
        self.female_names_first = self.load_data_from_csv(
            self.female_name_first_csv_path
        )
        self.female_names_second = self.load_data_from_csv(
            self.female_name_second_csv_path
        )
        self.female_surname = self.load_data_from_csv(self.female_surname_csv_path)

        self.font_path = self.data_path.joinpath("font", "Lato-Bold.ttf")

        self.font = ImageFont.truetype(self.font_path.as_posix(), 16)

    def load_data_from_csv(self, csv_path: Path) -> list:
        data_in_list = []
        with open(csv_path, "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                data_in_list.append(row[0].title())
        return data_in_list

    def generate_idcard(self) -> Tuple[ImageType, ImageType]:
        personality = self.get_personality()
        return self.generate_front_idcard(
            personality=personality
        ), self.generate_back_idcard(personality=personality)

    def generate_front_idcard(self, personality: Optional[dict] = None) -> ImageType:
        if not personality:
            personality = self.get_personality()
        id_card_img = Image.open(self.id_template_front_path)

        big_front_face_img = personality["face_img_gray"].resize(
            self.bbox_front_img_big_size
        )
        small_front_face_img = personality["face_img_gray"].resize(
            self.bbox_front_img_small_size
        )

        id_card_img = paste_img_with_blure(
            bg_img=id_card_img,
            img_to_paste=big_front_face_img,
            paste_point=(self.bbox_front_img_big[0], self.bbox_front_img_big[1]),
        )
        id_card_img = paste_img_with_blure(
            bg_img=id_card_img,
            img_to_paste=small_front_face_img,
            paste_point=(self.bbox_front_img_small[0], self.bbox_front_img_small[1]),
        )
        draw = ImageDraw.Draw(id_card_img)
        self.font = ImageFont.truetype(self.font_path.as_posix(), 50, encoding="unic")
        draw.text(self.bbox_surname, personality["surname"], "black", self.font)
        names = personality["first_name"] + " " + personality["second_name"]
        draw.text(self.bbox_first_name, names, "black", self.font)
        self.font = ImageFont.truetype(self.font_path.as_posix(), 35, encoding="unic")
        draw.text(self.bbox_family_name, personality["surname"], "black", self.font)
        parents_names = personality["father_name"] + " " + personality["mother_name"]
        draw.text(self.bbox_parents_names, parents_names, "black", self.font)
        draw.text(
            self.bbox_date_of_birth, personality["birth_date"], "black", self.font
        )
        sex_type = "M" if personality["is_male"] else "K"
        draw.text(self.bbox_sex, sex_type, "black", self.font)
        return id_card_img

    def generate_back_idcard(self, personality: Optional[dict] = None) -> ImageType:
        if not personality:
            personality = self.get_personality()
        id_card_img = Image.open(self.id_template_back_path)
        face_img = personality["face_img_gray"].resize(self.bbox_back_img_size)
        id_card_img = paste_img_with_blure(
            bg_img=id_card_img,
            img_to_paste=face_img,
            paste_point=(self.bbox_back_img[0], self.bbox_back_img[1]),
            blur_margin=7,
        )

        draw = ImageDraw.Draw(id_card_img)
        self.font = ImageFont.truetype(self.font_path.as_posix(), 45, encoding="unic")
        draw.text(self.bbox_pesel, personality["pesel"], "black", self.font)
        self.font = ImageFont.truetype(self.font_path.as_posix(), 25, encoding="unic")
        draw.text(self.bbox_nationality, "POLSKIE", "black", self.font)
        draw.text(self.bbox_place_of_birth, personality["place"], "black", self.font)
        draw.text(
            self.bbox_issuing_authority, personality["father_name"], "black", self.font
        )
        draw.text(
            self.bbox_id_card_number, personality["idcard_number"], "gray", self.font
        )
        draw.text(
            self.bbox_date_of_issue, personality["date_of_issue"], "black", self.font
        )
        draw.text(self.bbox_expiry_date, personality["expiry_date"], "black", self.font)
        self.font = ImageFont.truetype(self.font_path.as_posix(), 40, encoding="unic")
        back_code1 = self.genetrate_random_back_code()
        draw.text(self.bbox_back_end_code_line1, back_code1, "black", self.font)
        back_code2 = self.genetrate_random_back_code()
        draw.text(self.bbox_back_end_code_line2, back_code2, "black", self.font)
        back_code3 = self.genetrate_random_back_code()
        draw.text(self.bbox_back_end_code_line3, back_code3, "black", self.font)
        return id_card_img

    def get_personality(
        self,
    ) -> dict:
        is_male = bool(random.getrandbits(1))
        _, face_img_gray = self.get_random_face(is_male=is_male)
        first_name, second_name, surname = self.get_random_names(is_male=is_male)
        pesel, birth_date = self.generate_random_pesel_and_birth_date()
        father_name = random.choice(self.male_names_first)
        mother_name = random.choice(self.female_names_first)
        place = random.choice(self.male_names_first)
        date_of_issue = birth_date.split(".")
        date_of_issue[-1] = str(int(date_of_issue[-1]) + 20)
        expiry_date = date_of_issue
        expiry_date[-1] = str(int(date_of_issue[-1]) + 10)
        date_of_issue = ".".join(date_of_issue)
        expiry_date = ".".join(expiry_date)
        idcard_number = self.genetrate_random_idcard_number()
        return {
            "is_male": is_male,
            "face_img_gray": face_img_gray,
            "first_name": first_name,
            "second_name": second_name,
            "surname": surname,
            "pesel": pesel,
            "birth_date": birth_date,
            "father_name": father_name,
            "mother_name": mother_name,
            "place": place,
            "date_of_issue": date_of_issue,
            "expiry_date": expiry_date,
            "idcard_number": idcard_number,
        }

    def get_random_names(self, is_male: bool) -> Tuple[str, str, str]:
        if is_male:
            return self.get_random_male_names()
        return self.get_random_female_names()

    def get_random_male_names(self) -> Tuple[str, str, str]:
        first_name = random.choice(self.male_names_first)
        second_name = " "
        surname = random.choice(self.male_surname)
        if random.uniform(0, 1) > 0.5:
            second_name = random.choice(self.male_names_second)
        return first_name, second_name, surname

    def get_random_female_names(self) -> Tuple[str, str, str]:
        first_name = random.choice(self.female_names_first)
        second_name = " "
        surname = random.choice(self.female_surname)
        if random.uniform(0, 1) > 0.5:
            second_name = random.choice(self.female_names_second)
        return first_name, second_name, surname

    def generate_random_pesel_and_birth_date(self) -> Tuple[str, str]:
        year = random.randint(1930, 2099)
        if year <= 1999:
            month = random.randint(1, 12)
        elif year >= 2000:
            month = random.randint(1, 12) + 20  # to distinguish between centuries
        # I need to put months in a category to choose correct range of possible days for each one
        odd_months = (1, 3, 5, 7, 8, 10, 12, 21, 23, 25, 27, 28, 30, 32)
        even_months = (4, 6, 9, 11, 24, 26, 29, 31)
        if month in odd_months:
            day = random.randint(1, 31)

        elif month in even_months:
            day = random.randint(1, 30)
            # this is for february
        else:
            if year % 4 == 0 and year != 1900:
                day = random.randint(1, 29)  # leap year
            else:
                day = random.randint(1, 28)  # usual year
        four_random = random.randint(1000, 9999)
        four_random = str(four_random)
        # here comes the equation part, it calculates the last digit
        y = "%02d" % (year % 100)
        m = "%02d" % month
        dd = "%02d" % day
        a = y[0]
        a = int(a)
        b = y[1]
        b = int(b)
        c = m[0]
        c = int(c)
        d = m[1]
        d = int(d)
        e = dd[0]
        e = int(e)
        f = dd[1]
        f = int(f)
        g = four_random[0]
        g = int(g)
        h = four_random[1]
        h = int(h)
        i = four_random[2]
        i = int(i)
        j = four_random[3]
        j = int(j)
        check = a + 3 * b + 7 * c + 9 * d + e + 3 * f + 7 * g + 9 * h + i + 3 * j
        if check % 10 == 0:
            last_digit = 0
        else:
            last_digit = 10 - (check % 10)
        pesel = (
            str(year % 100) + str(month) + str(day) + str(four_random) + str(last_digit)
        )
        birth_date = f"{day}.{month}.{year}"
        return pesel, birth_date

    def genetrate_random_idcard_number(self):
        chars = string.ascii_uppercase
        digits = string.digits
        front = "".join(random.choice(chars) for _ in range(3))
        back = "".join(random.choice(digits) for _ in range(6))
        idcard_number = front + "   " + back
        return idcard_number

    def genetrate_random_back_code(self, lenght=32):
        chars = string.ascii_uppercase
        code = "".join(random.choice(chars) for _ in range(lenght))
        return code
