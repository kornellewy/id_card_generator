import os
import random
from typing import Tuple
import yaml
from pathlib import Path

from PIL import Image, ImageFilter


def load_files_with_given_extension(
    path, ext=[".jpg", ".png", ".jpeg"], name_format="path"
):
    images = []
    valid_images = ext
    for root, dirs, files in os.walk(path):
        for name in iter(files):
            ext = os.path.splitext(name)[1]
            if ext.lower() not in valid_images:
                continue
            # full path
            if name_format == "path":
                images.append(os.path.join(root, name))
            # jast its name
            elif name_format == "name":
                images.append(name)
            else:
                raise ValueError("wrong format for parameter : name_format")
    return images


def random_idx_with_exclude(exclude, idx_range):
    randInt = random.randint(idx_range[0], idx_range[1])
    return (
        random_idx_with_exclude(exclude, idx_range) if randInt in exclude else randInt
    )


def paste_img_with_blure(
    bg_img: Image,
    img_to_paste: Image,
    paste_point: tuple,
    blur_margin: int = 25,
) -> Image:
    bg_mask = Image.new("L", bg_img.size, 0)
    img_to_paste_mask = Image.new(
        "L",
        (img_to_paste.size[0], img_to_paste.size[1]),
        255,
    )
    img_to_paste = img_to_paste.resize(
        (img_to_paste.size[0] - blur_margin * 2, img_to_paste.size[1] - blur_margin * 2)
    )

    bg_img.paste(
        img_to_paste, (paste_point[0] + blur_margin, paste_point[1] + blur_margin)
    )
    bg_mask.paste(
        img_to_paste_mask,
        (paste_point[0], paste_point[1]),
    )
    blur = bg_img.filter(ImageFilter.GaussianBlur(radius=30))
    bg_img.paste(blur, mask=bg_mask)
    bg_img.paste(
        img_to_paste, (paste_point[0] + blur_margin, paste_point[1] + blur_margin)
    )
    return bg_img


def create_img_with_blur_edges(img_to_paste: Image, blur_margin: int = 30) -> Image:
    bg_image = Image.new("RGB", img_to_paste.size, (255, 255, 255))
    img_to_paste = img_to_paste.resize(
        (img_to_paste.size[0] - blur_margin * 2, img_to_paste.size[1] - blur_margin * 2)
    )
    bg_image.paste(
        img_to_paste,
        (blur_margin, blur_margin),
    )
    mask = Image.new("L", (bg_image.size[0], bg_image.size[1]), 255)
    image_bbox = Image.new(
        "L",
        (
            bg_image.size[0] - blur_margin * 2,
            bg_image.size[1] - blur_margin * 2,
        ),
        0,
    )
    mask.paste(image_bbox, (blur_margin, blur_margin))
    blur = bg_image.filter(ImageFilter.GaussianBlur(blur_margin / 2))
    bg_image.paste(blur, mask=mask)
    return bg_image


def random_digits(digits: int) -> int:
    lower = 10 ** (digits - 1)
    upper = 10 ** digits - 1
    return random.randint(lower, upper)


def read_yaml(yaml_file: Path) -> dict:
    with open(yaml_file, "r") as stream:
        yaml_data = yaml.safe_load(stream)
    return yaml_data


def read_label_file(label_path: Path) -> list:
    with open(label_path) as file:
        lines = [line.rstrip() for line in file]
    return lines
