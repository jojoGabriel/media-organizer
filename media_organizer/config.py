from dataclasses import dataclass
from pathlib import Path
from typing import Set


IMAGE_EXTENSIONS: Set[str] = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp",
    ".heic",
    ".heif",
    ".tif",
    ".tiff",
    ".dng",
    ".arw",
    ".cr2",
    ".nef",
}

VIDEO_EXTENSIONS: Set[str] = {
    ".mp4",
    ".mov",
    ".m4v",
    ".avi",
    ".mkv",
    ".webm",
    ".3gp",
    ".mts",
    ".m2ts",
    ".mpg",
    ".mpeg",
}

SIDECAR_EXTENSIONS: Set[str] = {".json"}

CACHE_DIRECTORY_NAMES: Set[str] = {".wdmc"}

SCREEN_RECORDING_PREFIXES = (
    "screenshot",
    "screenrecording",
    "screen recording",
    "vokoscreen",
    "obs ",
)

PROJECT_DIRECTORY_NAMES: Set[str] = {
    "pleasantharmony",
    "kali",
}


@dataclass(frozen=True)
class Roots:
    pictures: Path
    videos: Path

