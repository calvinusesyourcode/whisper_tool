import os, openai, subprocess, pathlib, math, datetime
from pathlib import Path
# my imports
from string_manipulation import to_time

def get_audio_size(filename: pathlib.WindowsPath):
    """Get the size of an audio file in MB."""
    cmd = ["ffprobe", '-i', filename, '-show_entries', 'format=size', '-v', 'quiet', '-of', 'csv=p=0']
    output = subprocess.check_output(cmd)
    return int(output)/1024/1024

def get_audio_duration(filename: pathlib.WindowsPath):
    """Get the duration of an audio file."""
    cmd = ['ffprobe', '-i', filename, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0']
    output = subprocess.check_output(cmd)
    return float(output)

def reformat_audio(folder,filename):
    """Reformat an audio file to 16kHz mono."""
    output_file = Path(folder,filename.stem+"_reformatted.mp3")
    command = ["ffmpeg", "-i", filename, "-vn", "-ac", "1", "-ar", "16000", "-ab", "192k", "-y", output_file]
    subprocess.run(command, check=True)
    os.remove(filename)
    return Path(output_file)


def split_audio_file(folder,filename):
    """Split an audio file into 24MB chunks, especially for use with Whisper API."""
    files = []
    filename = reformat_audio(folder,filename)
    output_title_stem = Path(filename).stem
    total_duration = get_audio_duration(filename)
    chunk_duration = int(get_audio_duration(filename)/(get_audio_size(filename)/24))
    num_chunks = math.ceil(total_duration / chunk_duration)
    
    for i in range(num_chunks):
        overlap = 2
        start_time = to_time(i * chunk_duration) if i == 0 else to_time((i * chunk_duration) - overlap)
        end_time = to_time(((i+1) * chunk_duration) + overlap)
        output = Path(f'{folder}/{output_title_stem}_{i}.mp3')
        cmd = ['ffmpeg', '-i', filename, '-ss', str(start_time), '-to', str(end_time), '-c', 'copy', output]
        subprocess.run(cmd, check=True)
        files.append(Path(output))
    os.remove(filename)
    return files