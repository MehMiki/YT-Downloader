from yt_dlp import YoutubeDL

def start_task(progress_bar, urls, folder, format_choice):
    links = [url.strip() for url in urls.split(",") if url.strip()]
    total = len(links)
    progress_bar['maximum'] = total
    progress_bar['value'] = 0

    for i, url in enumerate(links, start=1):
        try:
            if format_choice == "MP3":
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': f'{folder}/%(title)s.%(ext)s',   
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '256',
                    }],
                    'noplaylist': False,
                }

            elif format_choice == "MP4_AV":
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': f'{folder}/%(title)s.%(ext)s',
                    'merge_output_format': 'mp4',
                    'postprocessor_args': ['-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k'],
                    'noplaylist': False,
                }

            elif format_choice == "MP4_V":
                ydl_opts = {
                    'format': 'bestvideo/best',
                    'outtmpl': f'{folder}/%(title)s.%(ext)s',
                    'noplaylist': False,
                }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        except Exception as e:
            print(f"URL ERROR {url}: {e}")

        progress_bar['value'] = i
        progress_bar.master.update_idletasks()