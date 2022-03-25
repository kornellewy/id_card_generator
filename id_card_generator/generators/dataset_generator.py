from pathlib import Path

import cv2

from id_card_generator.generators.multiple_types_generator import (
    MultipleTypesGenerator,
)
from id_card_generator.utils.constans import TYPE_TO_IMAGE_NAME_MAP, IMG_EXTENSION


class DatasetGenerator:
    def generate_dataset(
        self,
        input_dataset_path: Path,
        output_dataset_path: Path,
        image_count_per_class: int,
    ) -> None:
        id_card_gen = MultipleTypesGenerator(dataset_path=input_dataset_path)
        output_dataset_path.mkdir(parents=True, exist_ok=True)
        for template_image_name, id_card_type in TYPE_TO_IMAGE_NAME_MAP.items():
            type_dir_path = output_dataset_path.joinpath(id_card_type)
            type_dir_path.mkdir(parents=True, exist_ok=True)
            for image_number in range(image_count_per_class):
                id_card = id_card_gen.generate_idcard(id_name=template_image_name)
                image_name = f"{image_number}{IMG_EXTENSION}"
                image_path = type_dir_path.joinpath(image_name)
                cv2.imwrite(image_path.as_posix(), id_card)
