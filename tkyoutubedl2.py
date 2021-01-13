'''
tkyoutubedl, version 2

Download your YouTube with a classic Tkinter UI.

(C) jkelol111 2020-present
'''

# Copyright information.
__author__ = 'jkelol111'
__copyright__ = '(C) jkelol111 2020-present'
__license__ = 'MIT License'
__version__ = '2.0.1'

# Import libraries.
# CHALLENGE: use only default Python 3 libraries (excluding pytube).
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import tkinter.ttk as ttk
import pathlib
import threading
import time
import pytube
import webbrowser
from localStoragePy import localStoragePy

localStorage = localStoragePy('tkyoutubedl2.jkelol111.me', 'sqlite')

def display_disclaimer(master=None):
    messagebox.showwarning('Obligatory disclaimer', 'By clicking OK, you accept to the following conditions:\n\nThis app is made as an educational project.\nThe author assumes 0 liability from the resources obtained via this app.\n\nPlease respect local laws and copyright. The author assumes no responsibility in any cases of lawful misconduct conducted via this app, you are on your own!', parent=master)


class TkYouTubeDlSettingsGUI:
    def __init__(self, root, settings, save_settings_cb):
        self.toplevel = tk.Toplevel(root)
        self.toplevel.title(f'TkYoutubeDl Settings {__version__}')
        self.toplevel.resizable(False, False)
        self.toplevel.protocol('WM_DELETE_WINDOW', self.save_settings)
        self.toplevel.bind('<Escape>', self.save_settings)
        self.toplevel.focus_set()
        self.toplevel.grab_set()

        self.settings = settings
        self.save_settings_cb = save_settings_cb

        application_settings_frame = tk.LabelFrame(self.toplevel, text='Application', padx=5, pady=5)
        tk.Label(application_settings_frame, text='Save directory: ').grid(row=0, column=0, sticky=tk.W)
        tk.Entry(application_settings_frame, textvariable=self.settings['save_dir']).grid(row=0, column=1, sticky=tk.NSEW)
        tk.Button(application_settings_frame, text='...', command=self.change_directory).grid(row=0, column=3, sticky=tk.NSEW)
        tk.Label(application_settings_frame, text='Download type:').grid(row=1, column=0, sticky=tk.W)
        tk.Radiobutton(application_settings_frame, text='Video', value='video', variable=self.settings['dl_type']).grid(row=2, column=0, sticky=tk.W)
        tk.Radiobutton(application_settings_frame, text='Audio', value='audio', variable=self.settings['dl_type']).grid(row=2, column=1, sticky=tk.W)
        application_settings_frame.grid(row=0, column=0, sticky=tk.EW, padx=10, pady=5)

        video_settings_frame = tk.LabelFrame(self.toplevel, text='Video downloads', padx=5, pady=5)
        tk.Label(video_settings_frame, text='Video quality: ').grid(row=0, column=0, sticky='w')
        tk.Entry(video_settings_frame, textvariable=self.settings['dl_video_quality']).grid(row=0, column=1, sticky=tk.NSEW)
        tk.Button(video_settings_frame, text='?', command=lambda: self.open_help('dl_video_quality')).grid(row=0, column=2, sticky=tk.EW)
        tk.Label(video_settings_frame, text='Video FPS: ').grid(row=1, column=0, sticky='w')
        tk.Entry(video_settings_frame, textvariable=self.settings['dl_video_fps']).grid(row=1, column=1, sticky=tk.NSEW)
        tk.Button(video_settings_frame, text='?', command=lambda: self.open_help('dl_video_fps')).grid(row=1, column=2, sticky=tk.EW)
        tk.Label(video_settings_frame, text='Video format: ').grid(row=2, column=0, sticky='w')
        tk.Entry(video_settings_frame, textvariable=self.settings['dl_video_format']).grid(row=2, column=1, sticky=tk.NSEW)
        tk.Button(video_settings_frame, text='?', command=lambda: self.open_help('dl_video_format')).grid(row=2, column=2, sticky=tk.EW)
        video_settings_frame.grid(row=1, column=0, sticky=tk.EW, padx=10, pady=5)

        audio_settings_frame = tk.LabelFrame(self.toplevel, text='Audio downloads', padx=5, pady=5)
        tk.Label(audio_settings_frame, text='Audio quality: ').grid(row=0, column=0, sticky='w')
        tk.Entry(audio_settings_frame, textvariable=self.settings['dl_audio_quality']).grid(row=0, column=1, sticky=tk.NSEW)
        tk.Button(audio_settings_frame, text='?', command=lambda: self.open_help('dl_audio_quality')).grid(row=0, column=2, sticky=tk.EW)
        tk.Label(audio_settings_frame, text='Audio format: ').grid(row=1, column=0, sticky='w')
        tk.Entry(audio_settings_frame, textvariable=self.settings['dl_audio_format']).grid(row=1, column=1, sticky=tk.NSEW)
        tk.Button(audio_settings_frame, text='?', command=lambda: self.open_help('dl_audio_format')).grid(row=1, column=2, sticky=tk.EW)
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
        display_disclaimer_label.bind('<Button-1>', lambda e: display_disclaimer(self.toplevel))
        display_disclaimer_label.grid(row=5, column=0, sticky='w')
        about_settings_frame.grid(row=3, column=0, sticky=tk.EW, padx=10, pady=5)

        tk.Button(self.toplevel, text='Clear settings', command=self.clear_settings).grid(row=4, column=0, sticky=tk.EW, padx=10, pady=5)

        self.toplevel.mainloop()

    def open_help(self, which):
        messagebox_title = 'Help: '
        messagebox_content = 'This setting controls the '
        if which == 'dl_video_quality':
            messagebox_title += 'Video quality'
            messagebox_content += 'quality of the video downloaded.\n\nSome suitable options are:\n-720p (Default)\n-480p\n-360p\n- etc.\n\nAs we have not implemented FFMPEG stiching for DASH files, you are usually restricted to 720p and below.'
        elif which == 'dl_video_fps':
            messagebox_title += 'Video FPS'
            messagebox_content += 'frame rate of the downloaded video.\n\nSome suitable options are:\n-60\n-30 (Default)\n\nThere might be more options available, you may try them.'
        elif which == 'dl_video_format':
            messagebox_title += 'Video format'
            messagebox_content += 'format of the downloaded video.\n\nSome suitable options are:\n-mp4 (Default)\n-webm\n\nThere might be more downloadable formats, you may try them.'
        elif which == 'dl_audio_quality':
            messagebox_title += 'Audio quality'
            messagebox_content += 'quality of the audio downloaded.\n\nSome suitable options are:\n-160kbps\n-128kbps (Default)\n-70kbps\n-50kbps\n\nThere might be more quality options available, you may try them.'
        elif which == 'dl_audio_format':
            messagebox_title += 'Audio format'
            messagebox_content += 'format of the downloaded audio.\n\nSome suitable options are:\n-mp4 (Default)\n-vorbis\n-opus\n\nThere might be more downloadable formats, you may try them.'
        messagebox.showinfo(messagebox_title, messagebox_content, parent=self.toplevel)
            

    def change_directory(self):
        selected_dir = filedialog.askdirectory(parent=self.toplevel)
        if selected_dir:
            self.settings['save_dir'].set(selected_dir)

    def save_settings(self, shim=None):
        self.save_settings_cb(self.settings)
        self.toplevel.destroy()

    def clear_settings(self):
        confirmation = messagebox.askyesno('Clear settings?', 'This will clear your settings!\n\nYou will have to redo the configuration.', parent=self.toplevel)
        if confirmation:
            for setting in self.settings:
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
                self.settings[setting].set(localStorage.getItem(setting))
        messagebox.showinfo('Reset complete', 'The settings have been refreshed to the factory defaults. This window is safe to close now.', parent=self.toplevel)

class TkYouTubeDlMain:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f'TkYouTubeDl {__version__}')
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.dl_total_size = 1

        # Layout inspiration: https://stackoverflow.com/questions/50422735/tkinter-resize-frame-and-contents-with-main-window
        buttonframe = tk.Frame(self.root, padx=10, pady=10)
        self.buttons = {
            'add': tk.Button(buttonframe, text='+', command=self.add_to_list),
            'remove': tk.Button(buttonframe, text=' - ', command=self.remove_from_list),
            'download': tk.Button(buttonframe, text='↓', command=self.start_download),
            'import': tk.Button(buttonframe, text=u'Import...', command=self.start_import_from_file),
            'settings': tk.Button(buttonframe, text=u'Settings...', command=self.open_settings)
        }
        button_counter = 0
        for button in self.buttons:
            self.buttons[button].grid(row=0, column=button_counter)
            button_counter += 1
        buttonframe.grid(row=0, column=0, sticky='ew')

        listbox_frame = tk.LabelFrame(self.root, text='To download:', padx=5, pady=5)
        self.listbox = tk.Listbox(listbox_frame, selectmode='browse')
        self.listbox.grid(row=0, column=0, sticky='ewns')
        listbox_scrollbar = tk.Scrollbar(listbox_frame, orient='vertical', command=self.listbox.yview)
        listbox_scrollbar.grid(row=0, column=1, sticky='ns')
        self.listbox.config(yscrollcommand=listbox_scrollbar.set)
        listbox_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='ewns')
        listbox_frame.rowconfigure(0, weight=1)
        listbox_frame.columnconfigure(0, weight=1)

        self.progressbar_frame_label = tk.StringVar()
        progressbar_frame = tk.LabelFrame(self.root, text='Download progress:', padx=5, pady=5)
        self.progressbar = ttk.Progressbar(progressbar_frame)
        self.progressbar.grid(row=0, column=0, sticky='ewns')
        self.downloading_item_label = tk.StringVar()
        self.downloading_item_label.set('Nothing downloading yet.')
        tk.Label(progressbar_frame, textvariable=self.downloading_item_label, justify='left').grid(row=1, column=0, sticky='w')
        progressbar_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky='ewns')
        progressbar_frame.rowconfigure(0, weight=1)
        progressbar_frame.columnconfigure(0, weight=1)

        self.settings = {
            'save_dir': tk.StringVar(self.root, value=localStorage.getItem('save_dir')),
            'dl_type': tk.StringVar(self.root, value=localStorage.getItem('dl_type')),
            'dl_video_quality': tk.StringVar(self.root, value=localStorage.getItem('dl_video_quality')),
            'dl_video_fps': tk.StringVar(self.root, value=localStorage.getItem('dl_video_fps')),
            'dl_video_format':  tk.StringVar(self.root, value=localStorage.getItem('dl_video_format')),
            'dl_audio_quality': tk.StringVar(self.root, value=localStorage.getItem('dl_audio_quality')),
            'dl_audio_format': tk.StringVar(self.root, value=localStorage.getItem('dl_audio_format'))
        }

        for setting in self.settings:
            if not self.settings[setting].get():
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
                self.settings[setting].set(localStorage.getItem(setting))

        if not localStorage.getItem('obligatory_disclaimer'):
            display_disclaimer()
            localStorage.setItem('obligatory_disclaimer', True)

        self.root.mainloop()

    def start_thread(self, function):
        t = threading.Thread(target=function)
        t.start()

    # Genius solution by Ohad Cohen: https://stackoverflow.com/questions/7014984/tkinter-tkmessagebox-not-working-in-thread
    def run_in_main_thread(self, fun, *args, **kwargs):
        def task_main_thread(fun, ret, args, kwargs):
            ret.append(fun( *args, **kwargs))
        ret = []
        sleeptime = kwargs.pop('sleeptime', 0.5)
        self.root.after(0, task_main_thread, fun, ret, args, kwargs)
        while not ret:
            time.sleep(sleeptime)
        return ret[0]

    def start_import_from_file(self):
        def task_import_from_file():
            listfile = filedialog.askopenfilename(filetypes=[('TkYouTubeDl Text List', '.txt')])
            if listfile:
                with open(listfile, 'r') as FileStream:
                    content = FileStream.read()
                    entries = content.split('\n')
                    for entry in entries:
                        self.listbox.insert(tk.END, entry)
        self.start_thread(task_import_from_file)


    def update_settings(self, settings):
        self.settings = settings
        for setting in self.settings:
            if localStorage.getItem(setting) != self.settings[setting].get():
                localStorage.setItem(setting, self.settings[setting].get())

    def open_settings(self):
        TkYouTubeDlSettingsGUI(self.root, self.settings, self.update_settings)

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

    def update_download_progress_bar(self, stream = None, chunk = None, remaining = None):
        self.progressbar['value'] = self.dl_total_size - remaining

    def start_download(self):
        if self.listbox.get(0):
            def task_start_download():
                try:
                    def download_complete_cb(stream=None, file_path=None):
                        self.dl_total_size = 0
                        self.progressbar.stop()
                        self.downloading_item_label.set('Nothing downloading yet.')
                        self.buttons['add'].config(state=tk.NORMAL)
                        self.buttons['remove'].config(state=tk.NORMAL)
                        self.buttons['download'].config(state=tk.NORMAL)
                        self.buttons['import'].config(state=tk.NORMAL)
                        self.buttons['settings'].config(state=tk.NORMAL)
                    for i, listbox_item in enumerate(self.listbox.get(0, tk.END)):
                        self.buttons['add'].config(state=tk.DISABLED)
                        self.buttons['remove'].config(state=tk.DISABLED)
                        self.buttons['download'].config(state=tk.DISABLED)
                        self.buttons['import'].config(state=tk.DISABLED)
                        self.buttons['settings'].config(state=tk.DISABLED)
                        self.downloading_item_label.set(listbox_item)
                        yt = pytube.YouTube(listbox_item, on_progress_callback=self.update_download_progress_bar, on_complete_callback=download_complete_cb)
                        self.downloading_item_label.set(yt.title)
                        dl_type = self.settings['dl_type'].get()
                        content = None
                        if dl_type == 'video':
                            content = yt.streams.filter(res=self.settings['dl_video_quality'].get(), fps=int(self.settings['dl_video_fps'].get()), file_extension=self.settings['dl_video_format'].get(), progressive=True).first()
                        elif dl_type == 'audio':
                            content = yt.streams.filter(abr=self.settings['dl_audio_quality'].get(), file_extension=self.settings['dl_audio_format'].get()).first()
                        else:
                            raise TypeError(f'Download type is invalid ({dl_type})')
                        if content:
                            print(f'{dl_type} is available!')
                            print(content)
                            self.dl_total_size = content.filesize
                            self.progressbar['maximum'] = content.filesize
                            print(f'Stored total: {self.dl_total_size}')
                            print(f'total: {content.filesize}')
                            content.download(self.settings['save_dir'].get(), skip_existing=False)
                            self.listbox.delete(i)
                        else:
                            download_complete_cb()
                            self.run_in_main_thread(lambda: messagebox.showerror('Content unvailable', f'The download for the requested content was not found with the current settings, or the content is not available on YouTube:\n\n"{yt.title}"\n\nPlease recheck your settings or video availability.'))
                            break
                except Exception as e:
                    download_complete_cb()
                    self.run_in_main_thread(lambda: messagebox.showerror('Download error', f'Download failed for unknown reason:\n\n{str(e)}'))
            self.start_thread(task_start_download)

if __name__ == '__main__':
    try:
        TkYouTubeDlMain()
    except KeyboardInterrupt:
        exit()