from pathlib import Path
from typing import Tuple, Dict, List, Optional
import random
from copy import copy, deepcopy

import cv2
import numpy as np

from id_card_generator.utils.base_image import BaseImage
from id_card_generator.utils.bbox import BBox
from id_card_generator.utils.constans import TYPE_TO_IMAGE_NAME_MAP
from id_card_generator.utils.utils import (
    read_yaml,
    load_files_with_given_extension,
    read_label_file,
    get_random_string,
)


class MultipleTypesGenerator:
    LABELS_DIR_NAME = "labels"
    FACES_DIR_PATH = Path("data/faces")
    FONT_COLOR = (0, 0, 0)
    FONT = cv2.FONT_HERSHEY_COMPLEX_SMALL
    FONT_THICKNES = 1

    def __init__(self, dataset_path: Path) -> None:
        self.dataset_path = dataset_path
        self.yaml_data = read_yaml(
            load_files_with_given_extension(dataset_path, ext=[".yaml"])[0]
        )
        self.classes = self.yaml_data["names"]
        self.idx_to_class, self.class_to_idx = self.load_maps()
        (
            self.images_dir_path,
            self.labels_dir_path,
        ) = self.load_labels_and_images_dir_path()
        self.images_paths = sorted(
            load_files_with_given_extension(self.images_dir_path)
        )
        self.labels_paths = sorted(
            load_files_with_given_extension(self.labels_dir_path, ext=[".txt"])
        )
        self.dataset = self.load_images_and_labels()
        self.face_dataset = self.load_face_images()

    def load_maps(self) -> Tuple[Dict[int, str], Dict[str, int]]:
        idx_to_class = {idx: class_name for idx, class_name in enumerate(self.classes)}
        class_to_idx = {class_name: idx for idx, class_name in enumerate(self.classes)}
        return idx_to_class, class_to_idx

    def load_labels_and_images_dir_path(self) -> Tuple[Path, Path]:
        images_dir_path = Path(self.dataset_path).joinpath(
            self.yaml_data["train"].replace("../", "")
        )
        labels_dir_path = images_dir_path.parent.joinpath(self.LABELS_DIR_NAME)
        return images_dir_path, labels_dir_path

    def load_images_and_labels(self) -> Dict[str, dict]:
        data = {}
        for image_path, label_path in zip(self.images_paths, self.labels_paths):
            image = BaseImage(image_path=Path(image_path), label_path=Path(label_path))
            bboxes = []
            label_lines = read_label_file(label_path=label_path)
            for label_line in label_lines:
                label_line = label_line.split(" ")
                bbox = BBox(
                    image_path=Path(image_path),
                    idx_to_class=self.idx_to_class,
                    yolo_line=label_line,
                )
                bboxes.append(bbox)
            image.bboxes = bboxes
            data[image.image_name] = image
        return data

    def load_face_images(self):
        face_images_paths = sorted(
            load_files_with_given_extension(self.FACES_DIR_PATH.as_posix())
        )
        faces_images = []
        for face_image_path in face_images_paths:
            faces_images.append(BaseImage(image_path=Path(face_image_path)))
        return faces_images

    def generate_idcard(self, id_name: Optional[str] = None) -> np.ndarray:
        if not id_name:
            id_name, id_image = random.choice(list(self.dataset.items()))
        else:
            id_image = self.dataset[id_name]
        for bbox in id_image.bboxes:
            # id_image.height, id_image.width
            bbox_data = bbox.get_coco()
            x_top_left = int(bbox_data["x_top_left"] * id_image.width)
            y_top_left = int(bbox_data["y_top_left"] * id_image.height)
            width = int(bbox_data["width"] * id_image.width)
            height = int(bbox_data["height"] * id_image.height)
            class_name = bbox_data["class_name"]
            if class_name == "img":
                face_img = deepcopy(random.choice(self.face_dataset))
                face_img.resize_image(new_width=width, new_height=height)
                face_img.image = cv2.cvtColor(face_img.image, cv2.COLOR_BGR2GRAY)
                face_img.image = cv2.cvtColor(face_img.image, cv2.COLOR_GRAY2RGB)
                id_image.image[
                    y_top_left : y_top_left + height, x_top_left : x_top_left + width
                ] = face_img.image
            elif class_name == "txt_change":
                # with computer vison technic
                # https://stackoverflow.com/questions/58349726/opencv-how-to-remove-text-from-background
                # and https://pyimagesearch.com/2020/05/18/image-inpainting-with-opencv-and-python/
                roi = id_image.image[
                    y_top_left : y_top_left + height, x_top_left : x_top_left + width
                ]
                roi_mask = self.get_roi_mask(roi=roi)
                roi = cv2.inpaint(roi, roi_mask, 5, flags=cv2.INPAINT_TELEA)
                font_size = self.get_max_font_size(roi_height=height)
                text_len = self.get_max_text_len(roi_width=width, font_size=font_size)
                roi = cv2.putText(
                    roi,
                    get_random_string(text_len),
                    (0, 15),
                    self.FONT,
                    font_size,
                    self.FONT_COLOR,
                    self.FONT_THICKNES,
                    cv2.LINE_AA,
                )
                id_image.image[
                    y_top_left : y_top_left + height, x_top_left : x_top_left + width
                ] = roi
        cv2.imshow("id_image.image", id_image.image)
        cv2.waitKey(0)
        return id_image.image

    def get_roi_mask(self, roi: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, close_kernel, iterations=1)
        dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
        dilate = cv2.dilate(close, dilate_kernel, iterations=1)
        return dilate

    def get_max_font_size(self, roi_height: int) -> int:
        font_size = 1
        for i in range(1, 15):
            font_size = i
            (_, text_height) = cv2.getTextSize(
                "M", self.FONT, font_size, self.FONT_THICKNES
            )[0]
            if text_height > roi_height:
                font_size = font_size - 1
                return font_size

    def get_max_text_len(self, roi_width: int, font_size: int) -> int:
        text_len = 1
        for i in range(1, 100):
            text_len = i
            (text_width, _) = cv2.getTextSize(
                get_random_string(text_len),
                self.FONT,
                font_size,
                self.FONT_THICKNES,
            )[0]
            if text_width > roi_width:
                text_len = text_len - 1
                return text_len
        return 0
