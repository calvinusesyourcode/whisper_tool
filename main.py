from pathlib import Path
import datetime, math, subprocess, os, torch, openai, pathlib
from requests_html import HTMLSession
from send2trash import send2trash

# my imports
from handle_youtube import find_videos, download_from_youtube, yt_urls_to_audiopath
from transcription import transcribe_via_api, transcribe_offline
from handle_audio import split_audio_file



def process_audios(paths:list, mode:str="offline"):

    if not os.path.exists(folder):
        os.makedirs(folder)

    with (open(f"log.txt", "a")) as f:
        f.write(f"\n{str(datetime.datetime.now())}\n")

    for i, path in enumerate(paths):
        
        os.system("cls")

        start = datetime.datetime.now()
        if mode == "offline":
            file = path
            result = transcribe_offline("medium.en", file)
            end = datetime.datetime.now()

            print(result)
            with (open(f"{folder}/{Path(file).stem}_text.txt", "w")) as f:
                f.write(result["text"])
            with (open(f"{folder}/{Path(file).stem}_segments.txt", "w")) as f:
                f.write(str(result["segments"]))
            with (open(f"log.txt", "a")) as f:
                f.write(f"Transcribed {Path(file)} with GPU in {end-start} seconds.\n")
            # send2trash(str(file))


folder = "output"
search_array = ["chatgpt and the nature of truth"]

# process_videos(find_videos("huberman", search_array))
# process_videos(find_videos("lex",search_array), "offline")

# process_audios(yt_urls_to_audiopath(["https://www.youtube.com/watch?v=jaH-dVr1GDM"]))
