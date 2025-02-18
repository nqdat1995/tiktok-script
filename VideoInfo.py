from typing import List, Optional
from Thumbnail import Thumbnail
from Version import Version

class VideoInfo:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)  # Dynamically set attributes