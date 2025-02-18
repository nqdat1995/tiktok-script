from typing import List, Optional

class Thumbnail:
    def __init__(self, url: Optional[str] = None, height: Optional[int] = None, width: Optional[int] = None):
        self.url = url
        self.height = height
        self.width = width