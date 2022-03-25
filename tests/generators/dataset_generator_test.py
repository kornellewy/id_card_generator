import unittest
import numpy as np
from pathlib import Path

from id_card_generator.generators.dataset_generator import (
    DatasetGenerator,
)


class DatasetGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.input_dataset_path = Path("data/multiple_types")
        self.output_dataset_path = Path("test_dataset")
        self.image_count_per_class = 1000

    def test_generate_idcard(self):
        generator = DatasetGenerator()
        generator.generate_dataset(
            input_dataset_path=self.input_dataset_path,
            output_dataset_path=self.output_dataset_path,
            image_count_per_class=self.image_count_per_class,
        )
        # self.assertIsInstance(id_card_img, np.ndarray)

    def tearDown(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()
