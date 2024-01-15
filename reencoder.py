import os
import sys
import subprocess
import shutil

def reencode(path: str, ext: str) -> None:
    for top_dir, directories, files in os.walk(path):
        for file in files:
            if file.lower().endswith(ext):
                origin_path: str = os.path.join(top_dir, file)
                out_path: str = os.path.join(top_dir, os.path.splitext(file)[0]+"_reenc.flac")
                command: list[str] = ["ffmpeg", "-i", origin_path, out_path]

                try:
                    subprocess.run(command, check=True)

                    os.remove(origin_path)
                    
                    shutil.move(out_path, origin_path)
                
                except subprocess.CalledProcessError as error:
                    sys.stderr.write(f"{file}\r\n{error}")



def main():
    argv: list[str] = os.argv
    
    dir_to_walk: str = ""
    ext_to_reencode: str = ".flac"
    valid_exts = ["flac", "mp3", "ogg", "aac"] #incomplete, look at ffmpeg docs or remove safety check

    if len(argv) < 2:
        dir_to_walk = os.getcwd()
    elif len(argv) < 3:
        if os.path.isdir(argv[1]):
            dir_to_walk = argv[1]
        else: return
    elif len(argv) < 4:
        if argv[2] in valid_exts:
            ext_to_reencode = f".{argv[2]}"
    reencode(dir_to_walk, ext_to_reencode)
    
main()