import unittest
import shutil
from PIL.Image import Image as ImageType

from id_card_generator.generators.multiple_types_generator import (
    MultipleTypesGenerator,
)


class PLType3IdcardGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dataset_path = "data/multiple_types"

    # def test_generate_idcard(self):
    #     generator = PLType3IdcardGenerator()
    #     id_card_front_img, id_card_back_img = generator.generate_idcard()
    #     self.assertIsInstance(id_card_front_img, ImageType)
    #     self.assertIsInstance(id_card_back_img, ImageType)

    def test_generate_idcard(self):
        generator = MultipleTypesGenerator(dataset_path=self.dataset_path)
        id_card_img = generator.generate_idcard()
        # self.assertIsInstance(id_card_img, ImageType)

    def tearDown(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()
