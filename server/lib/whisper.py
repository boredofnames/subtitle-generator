from subprocess import run


def generate_vtt(path, model, language, output_path="./tmp/vtt"):
    print(f"generating vtt with {model} in language {language}")
    vtt_command = f"whisper {path} --model {model} --language {language} --output_format vtt --output_dir {output_path}".split(
        " "
    )
    run(vtt_command)
