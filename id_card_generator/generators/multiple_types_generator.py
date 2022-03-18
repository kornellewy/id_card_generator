from pathlib import Path
from typing import Tuple, Dict, List

from id_card_generator.utils.utils import read_yaml, load_files_with_given_extension


class MultipleTypesGenerator:
    LABELS_DIR_NAME = "labels"
    
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

        self.images_paths = load_files_with_given_extension(self.images_dir_path)
        self.labels_paths = load_files_with_given_extension(
            self.labels_dir_path, ext=[".txt"]
        )



        print(self.images_paths)
        print(self.labels_paths)

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

    def load_label(self, label_path: Path) -> dict:
        
