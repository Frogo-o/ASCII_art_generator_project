import PySimpleGUI as sg
from PIL import Image, ImageGrab
import pyperclip
from .converter import image_to_ascii
from .utils import update_preview, copy_image_to_project_folder

def run_gui():
    sg.set_options(font=('Consolas', 12), background_color='#FFFFFF', text_color='#000000')

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

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "Load Image":
            path = values["-FILE-"]
            if path:
                try:
                    image = Image.open(path)
                    update_preview(image, window)
                    ascii_art = image_to_ascii(image, invert=values["-INVERT-"])
                    current_ascii = ascii_art
                    window["-OUTPUT-"].update(ascii_art)
                    copy_image_to_project_folder(path)
                except Exception as e:
                    sg.popup_error("Error loading image:", str(e))

        if event == "Paste from Clipboard":
            try:
                image = ImageGrab.grabclipboard()
                if image is None:
                    sg.popup_error("No image in clipboard.")
                else:
                    update_preview(image, window)
                    ascii_art = image_to_ascii(image, invert=values["-INVERT-"])
                    current_ascii = ascii_art
                    window["-OUTPUT-"].update(ascii_art)
            except Exception as e:
                sg.popup_error("Clipboard error:", str(e))

        if event == "Save to TXT" and current_ascii:
            save_path = sg.popup_get_file("Save ASCII Art", save_as=True, no_window=True, default_extension=".txt", file_types=(("Text Files", "*.txt"),))
            if save_path:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(current_ascii)
                sg.popup("Saved successfully!", save_path)

        if event == "Copy to Clipboard" and current_ascii:
            pyperclip.copy(current_ascii)
            sg.popup("ASCII art copied to clipboard!")

    window.close()
