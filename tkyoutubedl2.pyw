'''
tkyoutubedl, version 2

Download your YouTube with a classic Tkinter UI.

(C) jkelol111 2020-present
'''

# Copyright information.
__author__ = 'jkelol111'
__copyright__ = '(C) jkelol111 2020-present'
__license__ = 'Public Domain'
__version__ = '2.0.0'

# Import libraries.
# CHALLENGE: use only default Python 3 libraries (excluding pytube).
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import tkinter.ttk as ttk
import os
import pathlib
import threading
import time
import pytube
import webbrowser
from localStoragePy import localStoragePy

localStorage = localStoragePy('tkyoutubedl2.jkelol111.me')

settings = {
    'save_dir': localStorage.getItem('save_dir'),
    'dl_type': localStorage.getItem('dl_type'),
    'dl_video_quality': localStorage.getItem('dl_video_quality'),
    'dl_video_fps': localStorage.getItem('dl_video_fps'),
    'dl_video_format':  localStorage.getItem('dl_video_format'),
    'dl_audio_quality': localStorage.getItem('dl_audio_quality'),
    'dl_audio_format': localStorage.getItem('dl_audio_format')
}

def display_disclaimer(shim=None):
    messagebox.showwarning('Obligatory disclaimer', 'By clicking OK, you accept to the following conditions:\n\nThis app is made as an educational project.\nThe author assumes 0 liability from the resources obtained via this app.\n\nPlease respect local laws and copyright. The author assumes no responsibility in any cases of lawful misconduct conducted via this app, you are on your own!')

class TkYouTubeDlSettingsGUI:
    def __init__(self, root):
        self.toplevel = tk.Toplevel(root)
        self.toplevel.title(f'TkYoutubeDl Settings {__version__}')
        self.toplevel.resizable(False, False)
        self.toplevel.protocol('WM_DELETE_WINDOW', self.save_settings)
        self.toplevel.bind('<Escape>', self.save_settings)
        self.toplevel.focus_set()
        self.toplevel.grab_set()

        application_settings_frame = tk.LabelFrame(self.toplevel, text='Application', padx=5, pady=5)
        tk.Label(application_settings_frame, text='Save directory: ').grid(row=0, column=0, sticky=tk.W)
        tk.Entry(application_settings_frame, textvariable=settings['save_dir']).grid(row=0, column=1, sticky=tk.NSEW)
        tk.Button(application_settings_frame, text='...').grid(row=0, column=3, sticky=tk.NSEW)
        tk.Label(application_settings_frame, text='Download type:').grid(row=1, column=0, sticky=tk.W)
        tk.Radiobutton(application_settings_frame, text='Video', value='video', variable=settings['dl_type']).grid(row=2, column=0, sticky=tk.W)
        tk.Radiobutton(application_settings_frame, text='Audio', value='audio', variable=settings['dl_type']).grid(row=2, column=1, sticky=tk.W)
        application_settings_frame.grid(row=0, column=0, sticky=tk.EW, padx=10, pady=5)

        video_settings_frame = tk.LabelFrame(self.toplevel, text='Video downloads', padx=5, pady=5)
        tk.Label(video_settings_frame, text='Video quality: ').grid(row=0, column=0, sticky='w')
        tk.Entry(video_settings_frame, textvariable=settings['dl_video_quality']).grid(row=0, column=1, sticky=tk.NSEW)
        tk.Button(video_settings_frame, text='?').grid(row=0, column=2, sticky=tk.EW)
        tk.Label(video_settings_frame, text='Video FPS: ').grid(row=1, column=0, sticky='w')
        tk.Entry(video_settings_frame, textvariable=settings['dl_video_fps']).grid(row=1, column=1, sticky=tk.NSEW)
        tk.Button(video_settings_frame, text='?').grid(row=1, column=2, sticky=tk.EW)
        tk.Label(video_settings_frame, text='Video format: ').grid(row=2, column=0, sticky='w')
        tk.Entry(video_settings_frame, textvariable=settings['dl_video_format']).grid(row=2, column=1, sticky=tk.NSEW)
        tk.Button(video_settings_frame, text='?').grid(row=2, column=2, sticky=tk.EW)
        video_settings_frame.grid(row=1, column=0, sticky=tk.EW, padx=10, pady=5)

        audio_settings_frame = tk.LabelFrame(self.toplevel, text='Audio downloads', padx=5, pady=5)
        tk.Label(audio_settings_frame, text='Audio quality: ').grid(row=0, column=0, sticky='w')
        tk.Entry(audio_settings_frame, textvariable=settings['dl_audio_quality']).grid(row=0, column=1, sticky=tk.NSEW)
        tk.Button(audio_settings_frame, text='?').grid(row=0, column=2, sticky=tk.EW)
        tk.Label(audio_settings_frame, text='Audio format: ').grid(row=1, column=0, sticky='w')
        tk.Entry(audio_settings_frame, textvariable=settings['dl_audio_format']).grid(row=1, column=1, sticky=tk.NSEW)
        tk.Button(audio_settings_frame, text='?').grid(row=1, column=2, sticky=tk.EW)
        audio_settings_frame.grid(row=2, column=0, sticky=tk.EW, padx=10, pady=5)

        about_settings_frame = tk.LabelFrame(self.toplevel, text='About TkYouTubeDl', padx=5, pady=5)
        tk.Label(about_settings_frame, text=f'Version: {__version__}', font=('Helvetica', 12, 'bold')).grid(row=0, column=0, sticky='w')
        tk.Label(about_settings_frame, text='A downloader for YouTube videos coded in Python.').grid(row=1, column=0, sticky='w')
        tk.Label(about_settings_frame, text='Uses PyTube for YouTube video downloading.').grid(row=2, column=0, sticky='w')
        report_issue_label = tk.Label(about_settings_frame, text='Report an issue...', fg="blue", cursor="hand2", font=('Helvetica', 11, 'underline'))
        report_issue_label.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/jkelol111/tkyoutubedl/issues/new'))
        report_issue_label.grid(row=3, column=0, sticky='w')
        more_from_me_label = tk.Label(about_settings_frame, text='More from jkelol111...', fg="blue", cursor="hand2", font=('Helvetica', 11, 'underline'))
        more_from_me_label.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/jkelol111'))
        more_from_me_label.grid(row=4, column=0, sticky='w')
        display_disclaimer_label = tk.Label(about_settings_frame, text='View disclaimer...', fg="red", cursor="hand2", font=('Helvetica', 11, 'underline'))
        display_disclaimer_label.bind('<Button-1>', display_disclaimer)
        display_disclaimer_label.grid(row=5, column=0, sticky='w')
        about_settings_frame.grid(row=3, column=0, sticky=tk.EW, padx=10, pady=5)

        tk.Button(self.toplevel, text='Clear settings', command=self.clear_settings).grid(row=4, column=0, sticky=tk.EW, padx=10, pady=5)

        self.toplevel.mainloop()

    def save_settings(self, shim=None):
        for setting in settings:
            if localStorage.getItem(setting) != settings[setting].get:
                localStorage.setItem(setting, settings[setting].get())
        self.toplevel.destroy()

    def clear_settings(self):
        confirmation = messagebox.askyesno('Clear settings?', 'This will clear your settings!\n\nYou will have to redo the configuration.')
        print(confirmation)
        if confirmation:
            localStorage.clear()
            self.toplevel.destroy()

class TkYouTubeDlMainGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f'TkYouTubeDl {__version__}')
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.dl_total_size = 0

        # Layout inspiration: https://stackoverflow.com/questions/50422735/tkinter-resize-frame-and-contents-with-main-window
        buttonframe = tk.Frame(self.root, padx=10, pady=10)
        self.buttons = {
            'add': tk.Button(buttonframe, text='+', command=self.add_to_list),
            'remove': tk.Button(buttonframe, text=' - ', command=self.remove_from_list),
            'download': tk.Button(buttonframe, text='↓', command=self.start_download),
            'import': tk.Button(buttonframe, text=u'Import...'),
            'settings': tk.Button(buttonframe, text=u'Settings...', command=self.open_settings)
        }
        button_counter = 0
        for button in self.buttons:
            self.buttons[button].grid(row=0, column=button_counter)
            button_counter += 1
        buttonframe.grid(row=0, column=0, sticky='ew')

        listbox_frame = tk.LabelFrame(self.root, text='To download:', padx=5, pady=5)
        self.listbox = tk.Listbox(listbox_frame, selectmode='browse')
        with open('yt.txt', 'r') as FileStream:
            content = FileStream.read()
            entries = content.split('\n')
            for entry in entries:
                self.listbox.insert('end', entry)
        self.listbox.grid(row=0, column=0, sticky='ewns')
        listbox_scrollbar = tk.Scrollbar(listbox_frame, orient='vertical', command=self.listbox.yview)
        listbox_scrollbar.grid(row=0, column=1, sticky='ns')
        self.listbox.config(yscrollcommand=listbox_scrollbar.set)
        listbox_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='ewns')
        listbox_frame.rowconfigure(0, weight=1)
        listbox_frame.columnconfigure(0, weight=1)

        self.progressbar_frame_label = tk.StringVar()
        progressbar_frame = tk.LabelFrame(self.root, text='Download/import progress:', padx=5, pady=5)
        self.progressbar = ttk.Progressbar(progressbar_frame)
        self.progressbar.grid(row=0, column=0, sticky='ewns')
        self.downloading_item_label = tk.StringVar()
        self.downloading_item_label.set('Nothing downloading yet.')
        tk.Label(progressbar_frame, textvariable=self.downloading_item_label, justify='left').grid(row=1, column=0, sticky='w')
        progressbar_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky='ewns')
        progressbar_frame.rowconfigure(0, weight=1)
        progressbar_frame.columnconfigure(0, weight=1)

        for setting in settings:
            if not settings[setting]:
                if setting == 'save_dir':
                    localStorage.setItem('save_dir', pathlib.Path.home())
                elif setting == 'dl_type':
                    localStorage.setItem('dl_type', 'video')
                elif setting == 'dl_video_quality':
                    localStorage.setItem('dl_video_quality', '720p')
                elif setting == 'dl_video_fps':
                    localStorage.setItem('dl_video_fps', '30')
                elif setting == 'dl_video_format':
                    localStorage.setItem('dl_video_format', 'mp4')
                elif setting == 'dl_audio_quality':
                    localStorage.setItem('dl_audio_quality', '128kbps')
                elif setting == 'dl_audio_format':
                    localStorage.setItem('dl_audio_format', 'mp4')
            settings[setting] = tk.StringVar()
            settings[setting].set(localStorage.getItem(setting))

        if not localStorage.getItem('obligatory_disclaimer'):
            display_disclaimer()
            localStorage.setItem('obligatory_disclaimer', True)

        self.root.mainloop()

    def start_thread(self, function):
        t = threading.Thread(target=function)
        t.start()

    def runInGuiThreadAndReturnValue(self, fun, *args, **kwargs):
        def runInGui(fun, ret, args, kwargs):
            ret.append(fun( *args, **kwargs))
        ret = []
        sleeptime = kwargs.pop('sleeptime', 0.5)
        self.root.after(0, runInGui, fun, ret, args, kwargs)
        while not ret:
            time.sleep(sleeptime)
        return ret[0]

    def open_settings(self):
        TkYouTubeDlSettingsGUI(self.root)

    def add_to_list(self):
        url = simpledialog.askstring('Add YouTube video', 'URL of the YouTube video:', parent=self.root)
        if url and url.strip():
            self.listbox.insert(tk.END, url)
        elif not url:
            pass
        else:
            messagebox.showerror('No URL inputted', 'Please input the URL of the YouTube video you want to download.')
            self.add_to_list()

    def remove_from_list(self):
        self.listbox.delete('anchor')

    def update_progress_bar(self, stream=None, chunk=None, remaining=None, mode=None):
        if not mode:
            self.progressbar.stop()
            self.progressbar.config(mode='determinate')
            self.progressbar.config(value=self.dl_total_size - remaining)
        elif mode == 'indeterminate':
            self.progressbar.config(mode='indeterminate')
            self.progressbar.start()

    def start_download(self):
        if self.listbox.get(0):
            def task_start_download():
                try:
                    def download_complete_cb(stream=None, file_path=None):
                        self.dl_total_size = 0
                        self.update_progress_bar(remaining=0)
                        self.downloading_item_label.set('Nothing downloading yet.')
                        self.remove_from_list()
                        self.listbox.config(state=tk.NORMAL)
                        self.buttons['download'].config(state=tk.NORMAL)
                        self.buttons['remove'].config(state=tk.NORMAL)
                        self.buttons['settings'].config(state=tk.NORMAL)
                    global settings
                    self.buttons['remove'].config(state=tk.DISABLED)
                    self.buttons['settings'].config(state=tk.DISABLED)
                    self.buttons['download'].config(state=tk.DISABLED)
                    self.update_progress_bar(mode='indeterminate')
                    self.listbox.selection_set(0)
                    self.listbox.event_generate('<<ListboxSelect>>')
                    self.listbox.config(state=tk.DISABLED)
                    top_listbox_item = self.listbox.get(0)
                    self.downloading_item_label.set(top_listbox_item)
                    yt = pytube.YouTube(top_listbox_item, on_progress_callback=self.update_progress_bar, on_complete_callback=download_complete_cb)
                    self.downloading_item_label.set(yt.title)
                    dl_type = settings['dl_type'].get()
                    content = None
                    if dl_type == 'video':
                        content = yt.streams.filter(only_video=True, res=settings['dl_video_quality'].get(), fps=int(settings['dl_video_fps'].get()), file_extension=settings['dl_video_format'].get(), progressive=True)
                        
                    elif dl_type == 'audio':
                        content = yt.streams.filter(only_audio=True, abr=settings['dl_audio_quality'].get(), file_extension=settings['dl_audio_format'].get())
                    else:
                        messagebox.showerror('Download error', f'Download type is invalid ({dl_type})')
                        raise TypeError(f'Download type is invalid ({dl_type})')
                    # Check and create directory and download!
                    if content:
                        print(f'{dl_type} is available!')
                        content_todownload = content.first()
                        self.dl_file_size = content_todownload.filesize
                        self.progressbar.config(maximum=self.dl_total_size)
                        content_todownload.download(settings['save_dir'].get())
                    else:
                        download_complete_cb()
                        self.runInGuiThreadAndReturnValue(lambda: messagebox.showerror('Content unvailable', f'The download for the requested content was not found with the current settings, or the content is not available on YouTube:\n\n"{yt.title}"\n\nPlease recheck your settings or video availability.'))
                except Exception as e:
                    download_complete_cb()
                    self.runInGuiThreadAndReturnValue(lambda: messagebox.showerror('Download error', f'Download failed for unknown reason:\n\n{str(e)}'))
            self.start_thread(task_start_download)

if __name__ == '__main__':
    try:
        TkYouTubeDlMainGUI()
    except KeyboardInterrupt:
        exit()