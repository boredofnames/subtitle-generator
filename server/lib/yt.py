from subprocess import run


def get_audio(url, path):
    run(["yt-dlp", "-f", "worst", "-x", "--audio-format", "mp3", url, "-o", path])
