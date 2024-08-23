from subprocess import run


def get_video(url, path):
    run(["yt-dlp", "-f", "worst", url, "-o", path])
