import os
import subprocess
import json
from pathlib import Path
from typing import List
from DownloadYoutubeOption import DownloadYoutubeOption
from VideoInfo import VideoInfo
from YoutubeVideoType import YoutubeVideoType
from typing import List
import re

YTDLP_PATH = "yt-dlp"
YOUTUBE_URL = "https://www.youtube.com"

def get_list_videos(channel_url):
    print("Get channel info...")  # Tương đương OnMessageReceived

    channel_info: List[VideoInfo] = []
    arguments = [
        YTDLP_PATH,
        "--flat-playlist",
        "--print-json",
        "--extractor-args", "youtubetab:approximate_date",
        channel_url
    ]

    process = subprocess.Popen(
        arguments,
        stdout=subprocess.PIPE,
        text=True
    )

    for line in process.stdout:
        if line.strip():
            try:
                video_data = json.loads(line)
                video_info = VideoInfo(**video_data)
                channel_info.append(video_info)
            except json.JSONDecodeError:
                print("Error decoding JSON:", line)

    process.wait()
    print("Get channel info completed")
    return channel_info

def get_short_videos(channel_url: str) -> List[VideoInfo]:
    channel_info = get_list_videos(channel_url)  # Assume this is synchronous
    return [video for video in channel_info if video.playlist_webpage_url and video.playlist_webpage_url.lower().endswith("shorts")]

def get_normal_videos(channel_url: str) -> List[VideoInfo]:
    channel_info = get_list_videos(channel_url)  # Assume this is synchronous
    return [video for video in channel_info if video.playlist_webpage_url and video.playlist_webpage_url.lower().endswith("videos")]

def get_videos(options) -> List[VideoInfo]:
    channel_url = f"{YOUTUBE_URL}/{options.get("ChannelId")}"
    
    if options["VideoType"] == YoutubeVideoType.ALL:
        videos = get_list_videos(channel_url)
    elif options["VideoType"] == YoutubeVideoType.VIDEOS:
        videos = get_normal_videos(channel_url)
    elif options["VideoType"] == YoutubeVideoType.SHORTS:
        videos = get_short_videos(channel_url)
    else:
        videos = []

    if options.get("is_get_most_view"):
        videos = [video for video in videos if video.view_count and video.view_count >= options.view_num]

    return videos

def download_video(video_info, destination_path):
    try:
        output_file = "\"%(epoch)s-%(title)s.%(ext)s\""
        playlist_uploader_id = getattr(video_info, "playlist_uploader_id")
        video_url = getattr(video_info, "url")

        if not video_url:
            raise ValueError("Video URL is missing")

        target_path = os.path.join(destination_path, playlist_uploader_id)

        arguments = [
            YTDLP_PATH,
            "--no-embed-metadata", "--no-embed-thumbnail", "--no-playlist",
            "--no-warnings", "--no-mtime", "--no-write-comments",
            "--ppa", "ffmpeg:-threads 4", "-f", "bestvideo*+bestaudio/best",
            # "--concurrent-fragments", "10", "--limit-rate", "0",
            "--concurrent-fragments", "10",
            "--throttled-rate", "10M",
            # "--external-downloader", "aria2c",
            # "--external-downloader-args", "-s16 -x16 -k10M --quiet",
            "-P", target_path, "-o", output_file, video_url
        ]

        subprocess.run(arguments, shell=True)
        
    except Exception as ex:
        print(f"Error downloading video: {getattr(video_info, 'title')}\n{ex}")

import asyncio
import os
from pathlib import Path

def run_download(videos: List["VideoInfo"], options):
    try:
        print(f"Start process download video from channel {options['ChannelId']}")

        videos.sort(key=lambda x: getattr(x, "upload_date", 0) or 0, reverse=True)

        print(f"Total videos found: {len(videos)} videos")

        destination_path = Path(options["DestinationPath"]) / options["ChannelId"]
        
        if not os.path.exists(destination_path):
            os.mkdir(destination_path)
        
        #exists_files = set(f.name for f in destination_path.glob("*")) if destination_path.exists() else set()
        destination_files = {file.stem for file in destination_path.iterdir() if file.is_file()}

        for idx, video in enumerate(videos, start=1):
            print(f"Downloading....{idx}/{len(videos)}")

            video_title = getattr(video, "title", f"video_{idx}")
             
            if len(list(filter(lambda file_name: video_title in file_name, destination_files))) > 0:
                print(f"Video Existed. Skipped Video {idx}/{len(videos)}")
                continue

            download_video(video, options["DestinationPath"])
            
            print(f"Downloaded....{idx}/{len(videos)}")

        print(f"Complete process download video from channel {options["ChannelId"]}")

    except Exception as ex:
        print(f"Error occurred while downloading videos from channel {options["ChannelId"]}:\n{ex}")

options = {
    "ChannelId":"@StarryriverAnime",
    "DestinationPath":"D:/TIKTOK/YOUTUBE/",
    "IsGetMostView":False,
    "VideoType":YoutubeVideoType.SHORTS,
    "ViewNum" : 0
}

video_list = get_videos(options)

run_download(video_list, options)