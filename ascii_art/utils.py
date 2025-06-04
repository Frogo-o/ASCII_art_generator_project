import io
from PIL import Image

def update_preview(image: Image.Image, window, key="-IMG-"):
    bio = io.BytesIO()
    image.thumbnail((200, 200))
    image.save(bio, format="PNG")
    window[key].update(data=bio.getvalue())

