import PySimpleGUI as sg
from PIL import Image, ImageGrab, ImageDraw
import os
import io
import pyperclip

from .converter import image_to_ascii
from .utils import update_preview

def run_gui():
    sg.set_options(font=('Consolas', 12), background_color='#FFFFFF', text_color='#000000')

    blank_img = Image.new("RGB", (200, 100), color=(245, 245, 245))
    draw = ImageDraw.Draw(blank_img)
    draw.rectangle([(0, 0), (199, 99)], outline=(180, 180, 180))
    draw.text((50, 40), "No image", fill=(120, 120, 120))
    blank_bio = io.BytesIO()
    blank_img.save(blank_bio, format="PNG")
    blank_data = blank_bio.getvalue()

    current_image = None
    current_ascii = ""

    layout = [
        [sg.Text("Select image or paste from clipboard:")],
        [sg.Input(key="-FILE-", enable_events=True, readonly=True),
         sg.FileBrowse("Browse and Load", key="-BROWSE-", file_types=(("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"),))],
        [
            sg.Button("Paste from Clipboard"),
            sg.Button("Convert to ASCII"),
            sg.Button("Copy to Clipboard"),
            sg.Button("Clear")
        ],
        [
            sg.Text("Width:"),
            sg.Slider(range=(20, 200), default_value=100, orientation="h", key="-WIDTH-"),
            sg.Checkbox("Invert ASCII", default=False, key="-INVERT-")
        ],
        [sg.Column([[sg.Image(data=blank_data, key="-IMG-", size=(200, 100))]], key="-IMG-ROW-")],
        [sg.Column([[sg.Text("Width: 0 | Lines: 0", key="-INFO-")]], key="-INFO-ROW-")],
        [sg.Multiline(size=(100, 40), key="-OUTPUT-", disabled=True, autoscroll=True, expand_x=True, expand_y=True)]
    ]

    window = sg.Window(
        'ASCII Art Generator',
        layout,
        element_justification='center',
        finalize=True,
        location=(0, 0),
        resizable=True,
        size=sg.Window.get_screen_size()
    )

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "-FILE-":
            path = values["-FILE-"]
            if path:
                try:
                    image = Image.open(path)
                    current_image = image
                    update_preview(image, window)
                except Exception as e:
                    sg.popup_error("Error loading image:", str(e))

        if event == "-BROWSE-":
            path = values["-BROWSE-"]
            if path:
                try:
                    image = Image.open(path)
                    current_image = image
                    window["-FILE-"].update(path)
                    update_preview(image, window)
                except Exception as e:
                    sg.popup_error("Error loading image:", str(e))

        if event == "Paste from Clipboard":
            try:
                image = ImageGrab.grabclipboard()
                if image is None:
                    sg.popup_error("No image in clipboard.")
                else:
                    current_image = image
                    window["-FILE-"].update("")
                    update_preview(image, window)
            except Exception as e:
                sg.popup_error("Clipboard error:", str(e))

        if event == "Convert to ASCII":
            if current_image is not None:
                try:
                    ascii_art = image_to_ascii(
                        current_image,
                        new_width=int(values["-WIDTH-"]),
                        invert=values["-INVERT-"]
                    )
                    current_ascii = ascii_art
                    window["-OUTPUT-"].update(ascii_art)
                    window["-INFO-"].update(f"Width: {int(values['-WIDTH-'])} | Lines: {len(ascii_art.splitlines())}")
                except Exception as e:
                    sg.popup_error("Conversion failed:", str(e))
            else:
                sg.popup_error("No image loaded.")


        if event == "Copy to Clipboard":
            if current_ascii:
                try:
                    pyperclip.copy(current_ascii)
                    sg.popup("ASCII art copied to clipboard!")
                except Exception as e:
                    sg.popup_error("Clipboard copy failed:", str(e))

        if event == "Clear":
            current_ascii = ""
            current_image = None
            window["-OUTPUT-"].update("")
            window["-INFO-"].update("Width: 0 | Lines: 0")
            window["-IMG-"].update(data=blank_data)
            window["-FILE-"].update("")

    window.close()
