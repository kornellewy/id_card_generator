import unittest
import shutil

from id_card_generator.generators.base_generator import BaseGenerator


class BaseGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_face_images(self):
        generator = BaseGenerator()
        self.assertEqual(len(generator.face_images_paths), 8)

    def tearDown(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()
