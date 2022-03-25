import unittest
import numpy as np

from id_card_generator.generators.multiple_types_generator import (
    MultipleTypesGenerator,
)


class PLType3IdcardGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dataset_path = "data/multiple_types"

    def test_generate_idcard(self):
        generator = MultipleTypesGenerator(dataset_path=self.dataset_path)
        id_card_img = generator.generate_idcard()
        self.assertIsInstance(id_card_img, np.ndarray)

    def tearDown(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()
