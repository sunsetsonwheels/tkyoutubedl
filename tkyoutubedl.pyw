from tkinter import Tk, Toplevel, messagebox, Label, StringVar, HORIZONTAL, W, E, DISABLED, NORMAL
from tkinter.filedialog import askdirectory
from tkinter.ttk import Button, Progressbar, Entry, Radiobutton
from pytube import YouTube
from json import loads, dumps
from localStoragePy import localStoragePy
from os.path import isfile, abspath
from os import execl
from sys import executable, argv, exit
from pathlib import Path
from threading import Thread

def start_thread(function):
    t = Thread(target=function)
    t.start()

localStorage = localStoragePy("tkyoutubedl.jkelol111.me", "text")

if not localStorage.getItem("config.json"):
    createConfig = messagebox.askquestion("TkYoutubeDl Error", "We couldn't find your configuration file. Do you want to create one?")
    if createConfig == "yes":
        try:
            localStorage.setItem("config.json", dumps({"defaultFileDir": str(Path.home()),
                                                       "dlType": "video",
                                                       "dlQualityVideo": "720p",
                                                       "dlFPSVideo": 30,
                                                       "dlFormatVideo": "mp4",
                                                       "dlQualityAudio": "128kbps",
                                                       "dlFormatAudio": "mp4"}))
        except:
            messagebox.showerror("TkYoutubeDl error", "Could not make config file. The app will now quit.")
            exit()
        execl(executable, abspath(__file__), *argv) 
    else:
        messagebox.showerror("TkYoutubeDl error", "We couldn't find your configuration file. The app will now exit.")
        exit()
else:
    try:
        config_contents = loads(localStorage.getItem("config.json"))
        defaultFileDir = config_contents["defaultFileDir"]
        dlType = config_contents["dlType"]
        dlQualityVideo = config_contents["dlQualityVideo"]
        dlFPSVideo = config_contents["dlFPSVideo"]
        dlFormatVideo = config_contents["dlFormatVideo"]
        dlQualityAudio = config_contents["dlQualityAudio"]
        dlFormatAudio = config_contents["dlFormatAudio"]
    except Exception as e:
        messagebox.askretrycancel
        print(str(e))

def settings():
    currentDefaultDir = StringVar()
    currentDefaultDir.set(defaultFileDir)
    dlTypeChoice = StringVar()
    dlTypeChoice.set(dlType)
    currentVideoQuality = StringVar()
    currentVideoQuality.set(dlQualityVideo)
    currentVideoFPS = StringVar()
    currentVideoFPS.set(dlFPSVideo)
    currentVideoFormat = StringVar()
    currentVideoFormat.set(dlFormatVideo)
    currentAudioQuality = StringVar()
    currentAudioQuality.set(dlQualityAudio)
    currentAudioFormat = StringVar()
    currentAudioFormat.set(dlFormatAudio)
    def selectDefaultDir():
        dirSelected = askdirectory()
        if not dirSelected:
            pass
        else:
            currentDefaultDir.set(dirSelected)
    def saveSettings():
        global defaultFileDir
        global dlType
        global dlQualityVideo
        global dlFPSVideo
        global dlFormatVideo
        global dlQualityAudio
        global dlFormatAudio
        localStorage.setItem("config.json", '{"defaultFileDir": "'+currentDefaultDir.get()+'", "dlType": "'+dlTypeChoice.get()+'", "dlQualityVideo": "'+currentVideoQuality.get()+'", "dlFPSVideo": '+currentVideoFPS.get()+', "dlFormatVideo": "'+currentVideoFormat.get()+'", "dlQualityAudio": "'+currentAudioQuality.get()+'", "dlFormatAudio": "'+currentAudioFormat.get()+'"}')
        defaultFileDir = defualtDirEntry.get()
        dlType = dlTypeChoice.get()
        dlQualityVideo = currentVideoQuality.get()
        dlFPSVideo = int(currentVideoFPS.get())
        dlFormatVideo = currentVideoFormat.get()
        dlQualityAudio = currentAudioQuality.get()
        dlFormatAudio = currentAudioFormat.get()
        settingsWindow.destroy()
    def resetSettings():
        global defaultFileDir
        global dlType
        global dlQualityVideo
        global dlFPSVideo
        global dlFormatVideo
        global dlQualityAudio
        global dlFormatAudio
        localStorage.setItem("config.json", dumps({"defaultFileDir": str(Path.home()),
                                                   "dlType": "video",
                                                   "dlQualityVideo": "720p",
                                                   "dlFPSVideo": 30,
                                                   "dlFormatVideo": "mp4",
                                                   "dlQualityAudio": "128kbps",
                                                   "dlFormatAudio": "mp4"}))
        defaultFileDir = str(Path.home())
        dlType = "video"
        dlQualityVideo = "720p"
        dlFPSVideo = 30
        dlFormatVideo = "mp4"
        dlQualityAudio = "128kbps"
        dlFormatAudio = "mp4"
        settingsWindow.destroy()
    def videoSettings():
        videoSettingsWindow = Toplevel()
        videoSettingsWindow.wm_resizable(False, False)
        videoSettingsWindow.focus_set()
        videoSettingsWindow.grab_set()
        videoSettingsWindow["bg"] = "white"
        videoSettingsWindow.title("TkYoutubeDl settings")

        videoQualityLabel = Label(videoSettingsWindow, text="Video quality(<=720p):", font=("Segoe UI", 16))
        videoQualityLabel.grid(row=0, column=0, sticky=W)
        videoQualityEntry = Entry(videoSettingsWindow, textvariable=currentVideoQuality)
        videoQualityEntry.grid(row=1, column=0, sticky=W)

        videoFPSLabel = Label(videoSettingsWindow, text="Video FPS:", font=("Segoe UI", 16))
        videoFPSLabel.grid(row=2, column=0, sticky=W)
        videoFPS30Radiobutton = Radiobutton(videoSettingsWindow, text="30 FPS", variable=currentVideoFPS, value=30)
        videoFPS30Radiobutton.grid(row=3, column=0, sticky=W)
        videoFPS60Radiobutton = Radiobutton(videoSettingsWindow, text="60 FPS", variable=currentVideoFPS, value=60)
        videoFPS60Radiobutton.grid(row=4, column=0, sticky=W)
        if currentVideoFPS == 30:
            videoFPS30Radiobutton.invoke()
        elif currentVideoFPS == 60:
            videoFPS60Radiobutton.invoke()
        else:
            pass

        videoFormatLabel = Label(videoSettingsWindow, text="Video format:", font=("Segoe UI", 16))
        videoFormatLabel.grid(row=5, column=0, sticky=W)
        videoFormatEntry = Entry(videoSettingsWindow, textvariable=currentVideoFormat)
        videoFormatEntry.grid(row=6, column=0, sticky=W)

        videoOkButton = Button(videoSettingsWindow, text="Ok", command=lambda: videoSettingsWindow.destroy())
        videoOkButton.grid(row=7, column=0, sticky=W+E)
        videoSettingsWindow.mainloop()
    def audioSettings():
        audioSettingsWindow = Toplevel()
        audioSettingsWindow.wm_resizable(False, False)
        audioSettingsWindow.focus_set()
        audioSettingsWindow.grab_set()
        audioSettingsWindow["bg"] = "white"
        audioSettingsWindow.title("TkYoutubeDl settings")
        audioQualityLabel = Label(audioSettingsWindow, text="Audio quality:", font=("Segoe UI", 16))
        audioQualityLabel.grid(row=0, column=0, sticky=W)
        audioQualityEntry = Entry(audioSettingsWindow, textvariable=currentAudioQuality)
        audioQualityEntry.grid(row=1, column=0, sticky=W)
        audioFormatLabel = Label(audioSettingsWindow, text="Audio format:", font=("Segoe UI", 16))
        audioFormatLabel.grid(row=2, column=0, sticky=W)
        audioFormatEntry = Entry(audioSettingsWindow, textvariable=currentAudioFormat)
        audioFormatEntry.grid(row=3, column=0, sticky=W)
        audioOkButton = Button(audioSettingsWindow, text="Ok", command=lambda: audioSettingsWindow.destroy())
        audioOkButton.grid(row=4, column=0, sticky=W+E)
        audioSettingsWindow.mainloop()
    
    settingsWindow = Toplevel()
    settingsWindow.wm_resizable(False, False)
    settingsWindow.focus_set()
    settingsWindow.grab_set()
    settingsWindow["bg"] = "white"
    settingsWindow.title("TkYoutubeDl settings")

    defaultDirLabel = Label(settingsWindow, text="Default directory:", font=("Segoe UI", 16))
    defaultDirLabel.grid(row=0, column=0, sticky=W)
    defualtDirEntry = Entry(settingsWindow, textvariable=currentDefaultDir)
    defualtDirEntry.grid(row=1, column=0, sticky=W)
    defaultDirSelectButton = Button(settingsWindow, text="...", command=selectDefaultDir)
    defaultDirSelectButton.grid(row=1, column=1, sticky=E)

    dlTypeLabel = Label(settingsWindow, text="Download type:", font=("Segoe UI", 16))
    dlTypeLabel.grid(row=2, column=0, sticky=W)
    dlTypeVideoRadiobutton = Radiobutton(settingsWindow, text="Video", variable=dlTypeChoice, value="video")
    dlTypeVideoRadiobutton.grid(row=3, column=0, sticky=W)
    dlTypeAudioRadiobutton = Radiobutton(settingsWindow, text="Audio", variable=dlTypeChoice, value="audio")
    dlTypeAudioRadiobutton.grid(row=3, column=1, sticky=W)
    dlTypeVideoSettingsButton = Button(settingsWindow, text="Video settings", command=videoSettings)
    dlTypeVideoSettingsButton.grid(row=4, column=0, sticky=W)
    dlTypeAudioSettingsButton = Button(settingsWindow, text="Audio settings", command=audioSettings)
    dlTypeAudioSettingsButton.grid(row=4, column=1, sticky=W)

    saveSettingsButton = Button(settingsWindow, text="Save settings", command=saveSettings)
    saveSettingsButton.grid(row=5, column=0, sticky=W)
    resetSettingsButton = Button(settingsWindow, text="Reset settings", command=resetSettings)
    resetSettingsButton.grid(row=5, column=1, sticky=E)

    if dlTypeChoice.get() == "video":
        dlTypeVideoRadiobutton.invoke()
    elif dlTypeChoice.get() == "audio":
        dlTypeAudioRadiobutton.invoke()
    else:
        pass
    settingsWindow.mainloop()

dlFileSize = 0

def progress_check(stream = None, chunk = None, remaining = None):
    global dlFileSize
    dlProgressBar["value"] = dlFileSize - remaining
    raw_percent = ((dlFileSize - remaining)/dlFileSize)*100
    round_percent = round(raw_percent)
    root.title("TkYoutubeDl ("+str(round_percent)+"% Downloaded)")

def downloadVideo():
    dlComplete = False
    global dlFileSize
    root.title("TkYoutubeDl (Downloading...)")
    try:
        startDlButton.configure(state=DISABLED)
        settingsButton.configure(state=DISABLED)
        videoLinkEntry.configure(state=DISABLED)
        video = YouTube(videoLinkEntry.get(), on_progress_callback=progress_check)
        if dlType == "video":
            video2 = video.streams.filter(res=dlQualityVideo, mime_type="video/"+dlFormatVideo, fps=dlFPSVideo, progressive=True).first()
            if video2 == None:
                messagebox.showerror("TkYoutubeDl Error", "No videos match your download criteras. Please check your settings.")
            else:
                dlFileSize = video2.filesize
                dlProgressBar["maximum"] = dlFileSize
                video2.download(defaultFileDir)
                dlComplete = True
        elif dlType == "audio":
            audio2 = video.streams.filter(only_audio=True, abr=dlQualityAudio, mime_type="audio/"+dlFormatAudio).first()
            if audio2 == None:
                messagebox.showerror("TkYoutubeDl Error", "No videos match your download criteras. Please check your settings.")
            else:
                dlFileSize = audio2.filesize
                dlProgressBar["maximum"] = dlFileSize
                audio2.download(defaultFileDir)
                dlComplete = True
        dlProgressBar.stop()
        startDlButton.configure(state=NORMAL)
        settingsButton.configure(state=NORMAL)
        videoLinkEntry.configure(state=NORMAL)
        root.title("TkYoutubeDl")
        if dlComplete == True:
            messagebox.showinfo("TkYoutubeDl", "Download of '"+video.title+"' completed! The file is saved in '"+defaultFileDir+"'.")
    except Exception as e:
        startDlButton.configure(state=NORMAL)
        settingsButton.configure(state=NORMAL)
        videoLinkEntry.configure(state=NORMAL)
        dlProgressBar.stop()
        root.title("TkYoutubeDl")
        print(str(e))
        messagebox.showerror("TkYoutubeDl Error", "We failed to download your video. Perhaps check your network connection?\n\nError details:\n"+str(e))

root = Tk()
root.wm_resizable(False, False)
root.focus_set()
root.title("TkYoutubeDl")
root["bg"] = "white"

linkLabel = StringVar()

videoLinkEntry = Entry(root, textvariable=linkLabel)
videoLinkEntry.grid(row=0, column=0, sticky=W+E)
startDlButton = Button(root, text="Download!", command=lambda: start_thread(downloadVideo))
startDlButton.grid(row=0, column=1)

dlProgressBar = Progressbar(root, orient=HORIZONTAL, length=300, mode='determinate')
dlProgressBar.grid(row=1, column=0)
settingsButton = Button(root, text="Settings...", command=settings)
settingsButton.grid(row=1, column=1)

root.mainloop()