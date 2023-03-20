import unittest


class Test(unittest.TestCase):

    def test_init_image(self):
        from PIL import Image
        from models.card import init_image

        self.assertIsInstance(init_image(
            "./static/images/cat.jpeg"), Image.Image)
        self.assertIsInstance(init_image(
            "https://sun9-33.userapi.com/impg/IhNK--0Uq5nkNcGrTAKNLBTmlUCmlaGtKXA8mQ/lGWxhgtEWlI.jpg?size=1215x2160&quality=96&sign=81e4aafe084811308715e1b5cf017beb&c_uniq_tag=KSRWC3zDbEGwaTgP-6JfF-hyVoINDGWsUgFZ4LMi1ak&type=album"), Image.Image)
        self.assertIsInstance(init_image(Image.open(
            "./static/images/cat.jpeg")), Image.Image)
        self.assertRaises(FileNotFoundError, init_image, "some_random_string")

    def test_chain_image(self):
        pass


if __name__ == "__main__":
    unittest.main()
