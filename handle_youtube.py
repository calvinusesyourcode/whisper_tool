from pytube import YouTube
from pathlib import Path
import datetime, math, subprocess, os, torch, openai, pathlib, re
from requests_html import HTMLSession


def find_videos(channel,search_terms):
    """Find video URLs from a channel that match a search term.
    
    "lex" or "huberman" for channel"""
    
    url = {'lex': 'https://www.youtube.com/@lexfridman/videos',
            'huberman': 'https://www.youtube.com/@hubermanlab/videos'}[channel]
    
    #use the session to get the data
    s = HTMLSession().get(url)
    #Render the page, up the number on scrolldown to page down multiple times on a page
    s.html.render(sleep=1, keep_page=True, scrolldown=1)

    titles = []
    links = []
    divs = s.html.find('.ytd-two-column-browse-results-renderer',first=True).find("#primary",first=True).find(".ytd-rich-grid-renderer")#.find("#contents",first=True)
    for div in divs:
        if div.find("#contents",first=True):
            video_rows = div.find("#contents",first=True).find(".ytd-rich-grid-row")
            for i, row in enumerate(video_rows):
                try:
                    videos = row.find("#contents",first=True).find(".ytd-rich-item-renderer")
                    for k, video in enumerate(videos):
                        try:
                            metadata = video.find(".ytd-rich-item-renderer",first=True).find("#content",first=True).find(".ytd-rich-grid-media",first=True) \
                            .find("#dismissible",first=True).find("#details",first=True).find("#meta",first=True) \
                            .find("#video-title-link",first=True)
                            title = metadata.attrs["title"]
                            link = "https://www.youtube.com"+metadata.attrs["href"]
                            if title not in titles:
                                titles.append(title)
                                links.append(link)
                        except:
                            print('FAILED: video.find(".ytd-rich-item-renderer",first=True).find("#content",first=True).find(".ytd-rich-grid-media",first=True) \
                            .find("#dismissible",first=True).find("#details",first=True).find("#meta",first=True) \
                            .find("#video-title-link",first=True)')
                except:
                    print('FAILED: row.find("#contents",first=True).find(".ytd-rich-item-renderer")')
    video_urls = []
    for i, title in enumerate(titles):
        for search_term in search_terms:
            if search_term in title.lower():
                video_urls.append(links[i])
    os.system("cls")
    print("Got urls from HTML")
    return video_urls

def download_from_youtube(video_url:str, folder:pathlib.WindowsPath="downloads", mode:str="video", quality:str="good", okay_with_webm:bool=True):
    """
    Download video using pytube, returns youtube video title.
    
    Args:
        *video_url: URL of the video to download.
        folder: Destination folder.
        mode: Download mode. Can be "video" for video, "audio" for low quality audio. Defaults to "video".
        quality: Quality of the video. Can be "highest", "good" for 1080p, "medium" for 720p, "low" for 480p, "lowest". Defaults to "good".
        okay_with_webm: Defaults to True.

    Returns:
        str: A formatted title of the downloaded YouTube video.
    """

    if mode == "video":
        
        video_path = download_from_youtube(video_url, folder, mode="video_only", quality=quality, okay_with_webm=okay_with_webm)
        audio_path = download_from_youtube(video_url, folder, mode="audio", quality=quality, okay_with_webm=okay_with_webm)
        output_filename = Path(folder, str(video_path.stem)+"_.mp4")

        command = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac {output_filename}"
        subprocess.check_output(command, shell=True)
        os.remove(video_path)
        os.remove(audio_path)


    elif mode == "video_only":

        youtube_video = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
        
        videos = youtube_video.streams.filter(type="video")
        if okay_with_webm:
            videos = videos.filter(file_extension="webm")
        else:
            videos = videos.filter(file_extension="mp4")
        streams = sorted(videos, reverse=True, key=lambda stream: int(''.join(c for c in stream.resolution if c.isdigit())) if stream.resolution else 0)
        
        quality_map = {
            "highest": 999999,
            "good": 1080,
            "medium": 720,
            "low": 480,
            "lowest": 360,
        }
        selected_stream = next((stream for stream in streams if int(re.findall(r'\d+', stream.resolution)[0]) <= quality_map[quality]), None)
        for stream in streams:
            print(int(re.findall(r'\d+',stream.resolution)[0]))
        print(quality_map[quality])   

    elif mode == "audio":

        youtube_video = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)

        streams = sorted(youtube_video.streams.filter(only_audio=True, file_extension="mp4"), reverse=True, key=lambda stream: int(''.join(c for c in stream.abr if c.isdigit())) if stream.abr else 0)
        print("\n".join(str(stream) for stream in streams))

        quality_map = {
            "highest": 160000,
            "good": 128000,
            "medium": 70000,
            "low": 50000,
            "lowest": 48000,
        }
        
        selected_stream = next((stream for stream in streams if stream.bitrate <= quality_map[quality]), None)
        print(quality, quality_map[quality])
        print(selected_stream)
    else:
        raise Exception("Invalid mode. Must be 'video' or 'audio'.")
    
    if mode != "video":
        default_filename = selected_stream.default_filename
        without_extension = "".join(default_filename.split(".")[:-1])
        video_title = "_".join("".join(c.lower() for c in without_extension if c.isalnum() or c == " ").split(" "))
        file_extension = default_filename[-7:].split(".")[-1]
        output_filename = f"{video_title}.{file_extension}"
        
        selected_stream.download(output_path=folder, filename=output_filename)
    return Path(folder,output_filename)



download_from_youtube("https://www.youtube.com/watch?v=Sj3iI9jZCX8", folder="C:/Users/calvi/Desktop", mode="video", quality="good")

