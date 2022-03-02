import PySimpleGUI as sg
import os
import re
import shutil


sg.theme('DarkAmber')  # Add a touch of color

# Construction of the window.
# TODO Make this look good and user friendly
layout = [  [sg.Text('Folder location:')],
            [sg.In(enable_events=True, key="-FOLDER-"), sg.FolderBrowse()],  # Take as input the chosen folder absolute path
            [sg.Text('List of files: ')],
            [sg.Listbox(values=[], size=(30, 6), key='-FILES-')],
            [sg.Text('Name to filter:')],
            [sg.InputText(key="-NAME-"), sg.Button('Filter')],
            [sg.Text(key="-NEW_FOLDER-")],
            [sg.Listbox(values=[], size=(30, 6), key="-MATCHES-")],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Easy File Filter', layout)


# Get all files in directory
def get_file_names(path):
    file_names = []
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                file_names.append(entry.name)
        return file_names
    except FileNotFoundError:
        return ['No files found in ' + path]


# Check if a file match with a name
def get_matches(files, name):
    search_regex = r"{0}".format(name)
    matches_files = []
    for file in files:
        match = re.search(search_regex, file)

        if match:
            matches_files.append(file)

    return matches_files


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break

    # Update list to show all files in the directory
    if event == "-FOLDER-":
        window['-FILES-'].update(get_file_names(values['-FOLDER-']))

    # TODO Manage dumb filtering & already present folder
    #   [-] Filtering on nothing takes absolute path '/'
    #   [-] Filtering a file name with no matches create a directory
    if event == "Filter":
        files = get_file_names(values['-FOLDER-'])
        matches = get_matches(files, values['-NAME-'])

        filtered_files_path = values['-FOLDER-'] + '/' + values['-NAME-']

        os.mkdir(filtered_files_path)

        for match in matches:
            shutil.move(values['-FOLDER-'] + '/' + match, filtered_files_path)
            print('Moved file to /' + values['-NAME-'])

        window['-MATCHES-'].update(matches)  # Show matches files from filter
        window['-NEW_FOLDER-'].update('[!] Moved these files to /' + values['-NAME-'])

window.close()

