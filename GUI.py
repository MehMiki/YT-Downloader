from tkinter import *
from tkinter import filedialog, ttk
import threading
import main


#Functions

def chose_folder():
    global folder
    folder = filedialog.askdirectory()
    if folder:
        folder_label.config(text=folder)

def run_task():
    urls = links.get('1.0', END).strip()
    if not urls or not folder:
        status_label.config(text="Enter links and chose folder")
        return

    #progressbar and percent reset
    progress['value'] = 0
    percent_label.config(text="0%")
    status_label.config(text="Wait, downloading in progress...")

    choice = format_var.get()
    threading.Thread(target=download_thread, args=(urls, choice)).start()

def download_thread(urls, choice):
    links_list = [url.strip() for url in urls.split(",") if url.strip()]
    total = len(links_list)
    progress['maximum'] = total
    progress['value'] = 0

    for i, url in enumerate(links_list, start=1):
        main.start_task(progress, url, folder, choice)
        progress['value'] = i
        percent = int(i / total * 100)
        percent_label.config(text=f"{percent}%")
        progress.update_idletasks()

    status_label.config(text="All files downloaded!")

window = Tk()
logo = PhotoImage(file='images/GUI icon.png')
icon = PhotoImage(file='images/Download icon.png')
window.iconphoto(True, icon)
window.geometry("620x740")
window.title("YouTube Downloader")

Label(window, text="Youtube Downloader", font='Arial', fg='green', image=logo, compound='top').pack()

#Checkboxes
format_var = StringVar(value="MP4_AV")
frame = Frame(window)
frame.pack(pady=10)
Radiobutton(frame, text="MP3 - only audio", variable=format_var, value="MP3").pack(side=LEFT, padx=5)
Radiobutton(frame, text="MP4 - audio+video", variable=format_var, value="MP4_AV").pack(side=LEFT, padx=5)
Radiobutton(frame, text="MP4 - only video", variable=format_var, value="MP4_V").pack(side=LEFT, padx=5)

#Folder
Button(window, text="Chose folder", command=chose_folder).pack()
folder_label = Label(window, text="Folder not assigned")
folder_label.pack()

#URL-s widget
Label(window, text="Paste YT links (separate by comma if many)").pack()
links = Text(window, height=10)
links.pack(padx=10, pady=10, fill=BOTH, expand=True)

#Progressbar and percent info
progress_frame = Frame(window)
progress_frame.pack(pady=10)
progress = ttk.Progressbar(progress_frame, orient=HORIZONTAL, length=300, mode='determinate')
progress.pack(side=LEFT)
percent_label = Label(progress_frame, text="0%")
percent_label.pack(side=LEFT, padx=10)

#status
status_label = Label(window, text="")
status_label.pack()


Button(window, text='Download', font=('Calibri', 20), command=run_task).pack(pady=10)

Label(window, text="© 2025 MP For non-commercial and personal use only", font=('Arial', 10), fg='black', compound='bottom').pack(side='bottom')

folder = ""  #Folder variable

window.mainloop()