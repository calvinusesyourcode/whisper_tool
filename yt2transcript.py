from pathlib import Path
import datetime, math, subprocess, os, torch, openai, pathlib
from requests_html import HTMLSession

# my imports
from handle_youtube import find_videos, download_from_youtube
from transcription import transcribe_via_api, transcribe_offline
from audio_manipulation import split_audio_file



def process_videos(video_urls:list, mode:str="offline"):

    if not os.path.exists(folder):
        os.makedirs(folder)

    with (open(f"log.txt", "a")) as f:
        f.write(f"\n{str(datetime.datetime.now())}\n")

    for i, video_url in enumerate(video_urls):
        video_title = download_from_youtube(video_url,folder,mode="audio",quality="low",okay_with_webm=True)
        nice_title = "_".join(search_array[i].split(" "))
        
        os.system("cls")

        start = datetime.datetime.now()
        if mode == "offline":
            file = video_title
            result = transcribe_offline("small.en", file)
            end = datetime.datetime.now()

            print(result)
            with (open(f"{folder}/{Path(file).stem}_text.txt", "w")) as f:
                f.write(result["text"])
            with (open(f"{folder}/{Path(file).stem}_segments.txt", "w")) as f:
                f.write(str(result["segments"]))
            with (open(f"log.txt", "a")) as f:
                f.write(f"Transcribed {Path(file)} with GPU in {end-start} seconds.\n")
            # Clean up the downloaded files
            os.remove(file)


folder = "output"
search_array = ["chatgpt and the nature of truth"]

# process_videos(find_videos("huberman", search_array))
# process_videos(find_videos("lex",search_array), "offline")

process_videos(['https://www.youtube.com/watch?v=jclr0N6mvUI'])
