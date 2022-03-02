import PySimpleGUI as sg
import os
import re
import shutil

sg.theme('DarkAmber')  # Add a touch of color

# Construction of the window.
row1 = sg.Frame(' First step ',
                [
                    [sg.Text(), sg.Column([
                        [sg.Text('Folder location:')],
                        # Take as input the chosen folder absolute path
                        [sg.In(enable_events=True, key="-FOLDER-"), sg.FolderBrowse()],
                        [sg.Text('List of files: ')],
                        [sg.Listbox(values=[], size=(55, 10), key='-FILES-')],
                    ], size=(450, 300), pad=(0, 0))]
                ]
                )

row2 = sg.Frame(' Second step ',
                [
                    [sg.Text(), sg.Column([
                        [sg.Text('Name to filter:')],
                        [sg.InputText(key="-NAME-"), sg.Button('Filter')],
                        [sg.Text(key="-NEW_FOLDER-")],
                        [sg.Listbox(values=[], size=(55, 10), key="-MATCHES-")],
                    ], size=(450, 300), pad=(0, 0))]]
                )

layout = [
    [row1],
    [row2],
    [sg.Button('Quit')]
]

# Create the Window
window = sg.Window('Easy File Filter', layout, icon=os.getcwd() + "/EasyFileFilterIcon.ico")


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


# Create folder and move files to it
def move_files(source, destination, files):
    try:
        if not files:
            return "No files with this name where found"

        if source:  # Test that a real source folder is given
            os.mkdir(destination)
            for file in files:
                shutil.move(source + '/' + file, destination)

            return "[+] " + str(len(files)) + " Files moved in \n" + destination

        if not source:
            return "Please give a folder location"

    except FileExistsError:
        return "A folder with this name already exist"

    except PermissionError:
        return "Access denied, the program can't access this folder: " + source


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Quit':  # if user closes window or clicks quit
        break

    # Update list to show all files in the directory
    if event == "-FOLDER-":
        window['-FILES-'].update(get_file_names(values['-FOLDER-']))

    if event == "Filter":
        files = get_file_names(values['-FOLDER-'])
        matches = get_matches(files, values['-NAME-'])

        filtered_files_path = values['-FOLDER-'] + '/' + values['-NAME-']

        # Move files and store output
        # NOTE I think that this is not a clean way to do it, should improve concerned code later
        move_files_output = move_files(values['-FOLDER-'], filtered_files_path, matches)

        window['-MATCHES-'].update(matches)  # Show matches files from filter
        window['-NEW_FOLDER-'].update(move_files_output)  # Show the return of move_files

window.close()
