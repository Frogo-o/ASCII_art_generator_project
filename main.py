import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

import PySimpleGUI as sg

sg.set_options(
    font=('Consolas', 14),
    background_color='#FFFFFF',
    text_color='#000000',
)

layout = [[
    sg.Text(
        "Hello world!",
        font=('Consolas', 16),
        text_color='#333333',
        background_color='#FFFFFF',
        pad=(20,20)
    )
]]

window = sg.Window('Test', layout, element_justification='center', finalize=True)

while True:
    if window.read()[0] == sg.WIN_CLOSED:
        break
window.close()
