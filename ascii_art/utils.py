import io
import os
import shutil
from PIL import Image

def update_preview(image: Image.Image, window, key="-IMG-"):
    bio = io.BytesIO()
    image.thumbnail((200, 200))
    image.save(bio, format="PNG")
    window[key].update(data=bio.getvalue())

def copy_image_to_project_folder(image_path: str):
    shutil.copy(image_path, os.path.join(os.getcwd(), os.path.basename(image_path)))
