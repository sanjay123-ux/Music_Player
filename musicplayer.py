import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3
import threading
from pygame import mixer
import time

root = tk.ThemedTk()
root.get_themes()  # returns a list of all the themes that can be set
root.set_theme("radiance")  # Sets an available theme

# Fonts: Arial(corresponds to Helvetica), Courier New(Courier), Comic Sans Ms, Pixedays
# MS Sans Serif, MS Serif, Symbol, System,Times New Roman(Times) and Verdana
# Styles: Normal, bold, roman, italic, underline and overstrike

statusbar = ttk.Label(root, text="Welcome to Melody", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)

menubar = Menu(root)  # create the menubar at the root
root.config(menu=menubar)  # this will create menubar to be always at top and can accept submenu

submenu = Menu(menubar, tearoff=0)  # create submenu  at the menubar

playlist = []  # playlist: contains the filename+full path


# filename + full path is required to play the music inside play_music load function

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=browse_file)
submenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo("Melody", "This is a music player build using tkinter by @Sanjay Chauhan.")


submenu = Menu(menubar, tearoff=0)  # create submenu  at the menubar
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About us", command=about_us)

mixer.init()  # initializing  the mixer

root.title("Melody")
root.iconbitmap(r'images/melody.ico')

# Root Window: contains StatusBar, LeftFrame, RightFrame

leftframe = Frame(root)  # LeftFrame: contains Listbox
leftframe.pack(side=LEFT, padx=10, pady=10)

playlistbox = Listbox(leftframe)  # PlayListBox: contains only the filename
playlistbox.pack()

addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)


def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


delBtn = ttk.Button(leftframe, text="- Del", command=del_song)
delBtn.pack(side=LEFT)

rightframe = Frame(root)  # RightFrame: contains TopFrame, MiddleFrame and BottomFrame
rightframe.pack(pady=10)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text="Total Length : --:--")
lengthlabel.pack(pady=10)

currenttimelabel = ttk.Label(topframe, text="current Time : --:--", relief=GROOVE)
currenttimelabel.pack()


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length

    mins, secs = divmod(total_length, 60)  # div - total_length / 60 and mod - total_length % 60
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():  # mixer.music.get_busy:returns FALSE when we press STOP button(music stops)
        if paused:
            continue  # continue:ignores all the statements below it.We check if music is paused or not
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music resumed"
        paused = FALSE

    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' : ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror("Melody", "File not found. Please check again")


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music stopped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music paused"


def rewind_music():
    play_music()
    statusbar['text'] = "Music rewinded /restarted"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)  # set_volume function of mixer takes values from 0 to 1


muted = FALSE


def mute_music():
    global muted
    if muted:  # unmute the music
        set_vol(0.7)
        VolumeBtn.config(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        set_vol(0)
        VolumeBtn.config(image=mutePhoto)
        scale.set(0)
        muted = TRUE


middleframe = Frame(rightframe)
middleframe.pack(padx=30, pady=30)

playPhoto = PhotoImage(file="images/play.png")
PlayBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)  # Play button for the music player
PlayBtn.grid(row=0, column=0, padx=5)

stopPhoto = PhotoImage(file="images/stop.png")
StopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)  # Stop button for the music player
StopBtn.grid(row=0, column=1, padx=5)

pausePhoto = PhotoImage(file="images/pause.png")
PauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)  # Pause button for the music player
PauseBtn.grid(row=0, column=2, padx=5)

# bottom frame for volume, rewind, mute
bottomframe = Frame(rightframe)
bottomframe.pack()

rewindPhoto = PhotoImage(file="images/rewind.png")
RewindBtn = ttk.Button(bottomframe, image=rewindPhoto,
                       command=rewind_music)  # Rewind or Restart button for the music player
RewindBtn.grid(row=0, column=0)

mutePhoto = PhotoImage(file="images/mute.png")
volumePhoto = PhotoImage(file="images/volume.png")
VolumeBtn = ttk.Button(bottomframe, image=volumePhoto,
                       command=mute_music)  # Rewind or Restart button for the music player
VolumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL,
                  command=set_vol)  # Volume button for the music player
scale.set(70)  # implements the defaulst value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, padx=30, pady=20)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
