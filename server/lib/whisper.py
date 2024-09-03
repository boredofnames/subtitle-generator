from subprocess import run


def generate_vtt(path, model, lang, output_path="./tmp/vtt"):
    vtt_command = f"whisper {path} --model {model} --language {lang} --output_format vtt --output_dir {output_path}".split(
        " "
    )
    run(vtt_command)
