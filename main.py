import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

import PySimpleGUI as sg
from PIL import Image, ImageGrab
import os
import shutil
import io
import pyperclip

ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(image, new_width=100, invert=False):
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
        ]
        for pixel in pixels
    ])

    ascii_img = "\n".join([chars[i:i + new_width] for i in range(0, len(chars), new_width)])
    return ascii_img

sg.set_options(
    font=('Consolas', 12),
    background_color='#FFFFFF',
    text_color='#000000',
)

layout = [
    [sg.Text("Select image or paste from clipboard:")],
    [sg.Input(key="-FILE-", enable_events=True), sg.FileBrowse(file_types=(("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"),))],
    [sg.Button("Load Image"), sg.Button("Paste from Clipboard"), sg.Button("Save to TXT"), sg.Button("Copy to Clipboard")],
    [sg.Checkbox("Invert ASCII", default=False, key="-INVERT-")],
    [sg.Image(key="-IMG-", size=(200, 200))],
    [sg.Multiline(size=(100, 40), key="-OUTPUT-", disabled=True, autoscroll=True)]
]

window = sg.Window('ASCII Art Generator', layout, element_justification='center', finalize=True)

current_ascii = ""

def update_preview(image):
    bio = io.BytesIO()
    image.thumbnail((200, 200))
    image.save(bio, format="PNG")
    window["-IMG-"].update(data=bio.getvalue())

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "Load Image":
        path = values["-FILE-"]
        if path:
            try:
                image = Image.open(path)
                update_preview(image)
                ascii_art = image_to_ascii(image, invert=values["-INVERT-"])
                current_ascii = ascii_art
                window["-OUTPUT-"].update(ascii_art)
                shutil.copy(path, os.path.join(os.getcwd(), os.path.basename(path)))
            except Exception as e:
                sg.popup_error("Error loading image:", str(e))

    if event == "Paste from Clipboard":
        try:
            image = ImageGrab.grabclipboard()
            if image is None:
                sg.popup_error("No image in clipboard.")
            else:
                update_preview(image)
                ascii_art = image_to_ascii(image, invert=values["-INVERT-"])
                current_ascii = ascii_art
                window["-OUTPUT-"].update(ascii_art)
        except Exception as e:
            sg.popup_error("Clipboard error:", str(e))

    if event == "Save to TXT":
        if current_ascii:
            try:
                save_path = sg.popup_get_file("Save ASCII Art", save_as=True, no_window=True, default_extension=".txt", file_types=(("Text Files", "*.txt"),))
                if save_path:
                    with open(save_path, "w", encoding="utf-8") as f:
                        f.write(current_ascii)
                    sg.popup("Saved successfully!", save_path)
            except Exception as e:
                sg.popup_error("Failed to save:", str(e))

    if event == "Copy to Clipboard":
        if current_ascii:
            try:
                pyperclip.copy(current_ascii)
                sg.popup("✅ ASCII art copied to clipboard!")
            except Exception as e:
                sg.popup_error("Clipboard copy failed:", str(e))

window.close()
