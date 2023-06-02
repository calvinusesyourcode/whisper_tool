import datetime

def to_time(seconds):
    """Convert seconds to hh:mm:ss string, for use with ffmpeg."""
    return str(datetime.timedelta(seconds=seconds))
