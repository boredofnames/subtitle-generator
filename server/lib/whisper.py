from subprocess import run


def generate_vtt(path, model, lang):
    run(
        [
            "whisper",
            path,
            "--model",
            model,
            "--language",
            lang,
            "--output_format",
            "vtt",
            "--output_dir",
            "./tmp/vtt",
        ]
    )
