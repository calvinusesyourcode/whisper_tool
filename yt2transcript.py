from pathlib import Path
import datetime, math, subprocess, os, torch, openai, pathlib
from requests_html import HTMLSession

# my imports
from handle_youtube import find_videos, download_video
from transcription import transcribe_via_api, transcribe_offline
from audio_manipulation import split_audio_file



def process_videos(video_urls:list, mode:str):

    for i, video_url in enumerate(video_urls):
        video_title = download_video(video_url,folder)
        nice_title = "_".join(search_array[i].split(" "))
        files = split_audio_file(Path(f"{folder}/{video_title}"),nice_title)
        
        os.system("cls")
        print(video_title)
        print("\n".join(str(each) for each in files))


        for k, file in enumerate(files):
            print("\nTranscribing audio...")
            
            start = datetime.datetime.now()
            if mode == "online":
                result = transcribe_via_api(file)
            elif mode == "offline":
                result = transcribe_offline("base.en", file)
            end = datetime.datetime.now()

            print(result)
            with (open(f"output/{Path(file).stem}_text.txt", "w")) as f:
                f.write(result["text"])
            with (open(f"output/{Path(file).stem}_segments.txt", "w")) as f:
                f.write(str(result["segments"]))
            with (open(f"log.txt", "w")) as f:
                f.write(f"Transcribed {Path(file)} in {end-start} seconds.\n")
            # Clean up the downloaded files
            os.remove(file)


folder = "audio"
temporary_youtube_audio_name = "ytAudio.mp3"
search_array = ["how to breathe correctly"]

# process_videos(find_videos("huberman", search_array))
process_videos(["https://www.youtube.com/watch?v=NGgpSWcaV1U"], "offline")
