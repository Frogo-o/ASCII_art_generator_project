from PIL import Image

ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(image: Image.Image, new_width=100, invert=False) -> str:
    image = image.convert("L")
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    image = image.resize((new_width, new_height))

    pixels = image.getdata()
    scale = 256 // len(ASCII_CHARS)
    chars = "".join([
        ASCII_CHARS[
            len(ASCII_CHARS) - 1 - pixel // scale if invert else min(len(ASCII_CHARS) - 1, pixel // scale)
        ] for pixel in pixels
    ])
    return "\n".join([chars[i:i + new_width] for i in range(0, len(chars), new_width)])
