from enum import Enum

class AspectRatio(str, Enum):
    none = "None"
    widescreen = "16:9"
    standard = "4:3"
    widescreen_film = "2:1"
    portrait = "9:16"
    square = "1:1"
    standard_reverse = "3:4"
    
class VideoQuality(Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"