import PySimpleGUI as sg
from pytube import YouTube


start_layout = [
    [sg.Input("", key="-INPUT-"), sg.Button("Submit")]
]

sg.theme("DarkRed1")
info_tab = [
    [sg.Text("Title:"), sg.Text("", key="-TITLE-")],
    [sg.Text("Length:"), sg.Text("", key="-LENGTH-")],
    [sg.Text("Views:"), sg.Text("", key="-VIEWS-")],
    [sg.Text("Author:"), sg.Text("", key="-AUTHOR-")],
    [sg.Text("Description:"), sg.Multiline("", key="-DESCRIPTION-", size=(40, 20), no_scrollbar=True, disabled=True)]
]
download_tab = [
    [sg.Frame("Best Quality:", [[sg.Button("Download", key="-BEST-"), sg.Text("", key="-BESTRES-"), sg.Text("", key="-BESTSIZE-")]])],
    [sg.Frame("Worst Quality:", [[sg.Button("Download", key="-WORST-"), sg.Text("", key="-WORSTRES-"), sg.Text("", key="-WORSTSIZE-")]])],
    [sg.Frame("Audio:", [[sg.Button("Download", key="-AUDIO-"), sg.Text("", key="-AUDIOSIZE-")]])],
    [sg.VPush()],
    [sg.ProgressBar(100, size=(20, 20), expand_x=True, key="-PROGRESS-")]
]
layout = [
    [sg.TabGroup([[sg.Tab("Info", info_tab), sg.Tab("Download", download_tab)]])]
]
window = sg.Window("Youtube application", start_layout)
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Submit":
        video_object = YouTube(values["-INPUT-"])
        window.close()
        window = sg.Window("Youtube application", layout, finalize=True)

        #info
        window["-TITLE-"].update(video_object.title)
        window["-LENGTH-"].update(f"{video_object.length // 3600}:{video_object.length // 60 % 60 : 02n}:{video_object.length % 60}")
        window["-VIEWS-"].update(video_object.views)
        window["-AUTHOR-"].update(video_object.author)
        window["-DESCRIPTION-"].update(video_object.description)
        #download
        window["-BESTSIZE-"].update(f"{video_object.streams.get_highest_resolution().filesize / 1048576 : 1f} MB")
        window["-BESTRES-"].update(video_object.streams.get_highest_resolution().resolution)
        window["-WORSTSIZE-"].update(f"{video_object.streams.get_lowest_resolution().filesize / 1048576 : 1f} MB")
        window["-WORSTRES-"].update(video_object.streams.get_lowest_resolution().resolution)
        window["-AUDIOSIZE-"].update(f"{video_object.streams.get_audio_only().filesize / 1048576 : 1f} MB")
    elif event == "-BEST-":
        video_object.streams.get_highest_resolution().download()
    elif event == "-WORST-":
        video_object.streams.get_lowest_resolution().download()
    elif event == "-AUDIO-":
        video_object.streams.get_audio_only().download()

window.close()
