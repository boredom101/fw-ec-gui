import base64
import PySimpleGUI as sg
from sys import platform

import backend

icon = base64.b64encode(open("framework.png", "rb").read())

sg.set_options(font=("Courier New", 12))

backend = backend.Backend()

def LedControl(name):
    return [
        sg.Input(key="Input " + name, visible=False, enable_events=True, default_text="#000000"),
        sg.ColorChooserButton("Choose Color"),
        sg.Text('#000000', text_color="#000000", key="Display " + name),
        sg.Button("Set " + name),
    ]

def FanFrame():
    return sg.Frame("Fan Controls", [[
        sg.Checkbox("Manual Fan Control", enable_events=True, key="FanMode"),
        sg.Slider((0, 100), 0, 1, orientation='h', disable_number_display=True, enable_events=True, disabled=True, key="FanDuty")
    ]])

def CommandFrame():
    return sg.Frame("Command Controls", [[
        sg.Input(key="CommandPath", enable_events=True),
        sg.FileBrowse("Command Path")
    ]])

def LedFrame(names):
    controls = []
    for name in names:
        controls.append(LedControl(name))
    return sg.Frame("LED Controls", controls)

layout = [[
    CommandFrame(),
    FanFrame()
], [
    LedFrame(["left", "right", "power"])
]]

window = sg.Window("Framework Control", layout, element_justification="left", icon=icon)

while True:
    event, values = window.read()
    if isinstance(event, str):
        if event.startswith("Input "):
            window["Display " + event.split(" ")[1]].update(values[event], text_color=values[event])
        elif event.startswith("Set "):
            name = event.split(" ")[1]
            value = values["Input " + name]
            backend.change_color(name, int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16))
        elif event == "FanMode":
            if values["FanMode"]:
                window["FanDuty"].update(disabled=False)
                backend.fan(values["FanDuty"])
            else:
                window["FanDuty"].update(disabled=True)
                backend.fan(-1)
        elif event == "FanDuty":
            backend.fan(values["FanDuty"])
        elif event == "CommandPath":
            backend.set(values["CommandPath"], (platform == "linux" or platform == "linux2"))
    elif event == sg.WIN_CLOSED:
        break

window.close()