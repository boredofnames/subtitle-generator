from subprocess import run


def get_video(url, path):
    download_command = f"yt-dlp -f worst {url} -o {path}".split(" ")
    run(download_command)
