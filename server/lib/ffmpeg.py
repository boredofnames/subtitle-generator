from subprocess import run

def segment_audio(path, duration):
    output_path = path.replace("tmp/", "tmp/segments/").replace(".mp3", "")
    print(output_path)
    run(["ffmpeg", "-i", path, "-f", "segment", "-segment_time", str(duration), output_path + "_%03d.mp3"])