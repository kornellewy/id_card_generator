import unittest
import shutil
from PIL.Image import Image as ImageType

from id_card_generator.generators.pl_type_3_idcard_generator import (
    PLType3IdcardGenerator,
)


class PLType3IdcardGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    # def test_generate_idcard(self):
    #     generator = PLType3IdcardGenerator()
    #     id_card_front_img, id_card_back_img = generator.generate_idcard()
    #     self.assertIsInstance(id_card_front_img, ImageType)
    #     self.assertIsInstance(id_card_back_img, ImageType)

    def test_generate_front_idcard(self):
        generator = PLType3IdcardGenerator()
        id_card_img = generator.generate_front_idcard()
        self.assertIsInstance(id_card_img, ImageType)

    def test_generate_back_idcard(self):
        generator = PLType3IdcardGenerator()
        id_card_img = generator.generate_back_idcard()
        id_card_img.show()
        self.assertIsInstance(id_card_img, ImageType)

    def tearDown(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()
