import os
import shutil

from id_card_generator.utils.utils import load_files_with_given_extension


def convert_all_images_to_png(path: str) -> None:
    target_ext = ".png"
    images_paths = load_files_with_given_extension(path=path)
    for image_path in images_paths:
        if not image_path.endswith(target_ext):
            base_imagePath = os.path.splitext(image_path)[0]
            new_image_path = base_imagePath + target_ext
            shutil.copy2(image_path, new_image_path)
            os.remove(image_path)


if __name__ == "__main__":
    path = "data"
    convert_all_images_to_png(path=path)
