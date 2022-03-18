from pathlib import Path

from id_card_generator.utils.utils import read_yaml, load_files_with_given_extension


class MultipleTypesGenerator:
    def __init__(self, dataset_path: Path) -> None:
        self.dataset_path = dataset_path

        self.yaml_data = read_yaml(
            load_files_with_given_extension(dataset_path, ext=[".yaml"])[0]
        )
        self.classes = self.yaml_data["names"]
        self.idx_to_class = {
            idx: class_name for idx, class_name in enumerate(self.classes)
        }
        self.class_to_idx = {
            class_name: idx for idx, class_name in enumerate(self.classes)
        }

        self.images_dir_path = Path(self.dataset_path).joinpath(
            self.yaml_data["train"].replace("../", "")
        )
        self.labels_dir_path = self.images_dir_path.parent.joinpath("labels")

        self.images_paths = load_files_with_given_extension(self.images_dir_path)
        self.labels_paths = load_files_with_given_extension(
            self.labels_dir_path, ext=[".txt"]
        )

        print(self.images_paths)
        print(self.labels_paths)
    