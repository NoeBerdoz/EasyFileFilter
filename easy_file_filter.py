import PySimpleGUI as sg
import os


sg.theme('DarkAmber')  # Add a touch of color

# Construction of the window.
layout = [  [sg.Text('Folder location')],
            [sg.In(enable_events=True, key="-FOLDER-"), sg.FolderBrowse()],  # Take as input the chosen folder absolute path
            [sg.Listbox(values=[], size=(30, 6), key='-FILES-')],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Easy File Filter', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break

    # Update list to show all files in the directory
    if event == "-FOLDER-":

        # Get all files in directory
        file_names = []
        with os.scandir(values['-FOLDER-']) as entries:
            for entry in entries:
                file_names.append(entry.name)

        window['-FILES-'].update(file_names)

window.close()

