import unittest
from PIL import Image
from ascii_art.converter import image_to_ascii


class TestAsciiConverter(unittest.TestCase):

    def test_output_not_empty(self):
        image = Image.new("RGB", (10, 10), color=(128, 128, 128)) 
        ascii_art = image_to_ascii(image, new_width=10)
        self.assertRegex(ascii_art, r'[^\s]', "ASCII art should contain non-whitespace characters.")

    def test_ascii_line_count(self):
        image = Image.new("RGB", (10, 20), color="black")
        ascii_art = image_to_ascii(image, new_width=10)
        lines = ascii_art.splitlines()
        self.assertGreater(len(lines), 0)

    def test_invert_flag(self):
        image = Image.new("RGB", (10, 10), color="black")
        ascii_normal = image_to_ascii(image, new_width=10, invert=False)
        ascii_inverted = image_to_ascii(image, new_width=10, invert=True)
        self.assertNotEqual(ascii_normal, ascii_inverted)


if __name__ == "__main__":
    unittest.main()
