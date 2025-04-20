from pathlib import Path
import subprocess
import os

def edit_video(video_name, option):
    builder = []
    filter_builder = []

    builder.append(f"-y -i \"{os.path.join(option['OriginVideoPath'], video_name)}\"")
    filter_builder.append(
        f"[0:v]setpts={1 / option['VideoSpeed']:.4f}*PTS,"
        f"scale=1080:1920:force_original_aspect_ratio=decrease,"
        f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black[vid]; "
        f"[0:a]atempo={option['VideoSpeed']}[audio];"
    )
    
    # filter_builder.append(
    #     f"[0:v]setpts={1 / option['VideoSpeed']:.4f}*PTS,"
    #     f"scale=1080:1920:force_original_aspect_ratio=decrease,"
    #     f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2[fg];"
    #     f"[0:v]scale=1080:1920,boxblur=10:5[bg];"
    #     f"[bg][fg]overlay=(W-w)/2:(H-h)/2[vid];"
    #     f"[0:a]atempo={option['VideoSpeed']}[audio];"
    # )
    
    if option.get("OverlayFilePath"):
        builder.append(f"-i \"{option['OverlayFilePath']}\"")
        filter_builder.append(
            f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase," 
            f"crop=1080:1920,format=rgba," 
            f"colorchannelmixer=aa={option['Opacity'] / 100:.2f}[scaledA];"
        )

    if option.get("LogoFilePath"):
        builder.append(f"-i \"{option['LogoFilePath']}\"")
        filter_builder.append(
            f"[2:v]scale=iw*{option['LogoScale'] / 100:.2f}:-1,setsar=1[logo];"
        )

    final_video = 'vid'
    if option.get("OverlayFilePath") and option.get("LogoFilePath"):
        filter_builder.append(
            "[vid][scaledA]overlay[vidA]; "
            "[vidA][logo]overlay=" f"{option['LogoLocationX']}:{option['LogoLocationY']}[outv];"
        )
        final_video = 'outv'
    elif option.get("OverlayFilePath"):
        filter_builder.append(
            "[vid][scaledA]overlay[vidA]; "
        )
        final_video = 'vidA'
    elif option.get("LogoFilePath"):
        filter_builder.append(
            "[vid][logo]overlay=" f"{option['LogoLocationX']}:{option['LogoLocationY']}[vidB];"
        )
        final_video = 'vidA'

    builder.append(f"-filter_complex \"{''.join(filter_builder)}\"")    
    builder.append(
        f"-map \"[{final_video}]\" -map \"[audio]\" -c:v libx264 -preset fast -crf 23 "
        f"-c:a aac -b:a 128k \"{os.path.join(option['EditedVideoPath'], os.path.splitext(video_name)[0])}.mp4\""
    )

    command = " ".join(builder)
    subprocess.run(f"ffmpeg {command}", shell=True)
    print(command)

def run_edit_video(video_folder, destination_folder):
    if not os.path.exists(video_folder):
        os.mkdir(video_folder)
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)
        
    video_path = Path(video_folder)
    video_files = [file for file in video_path.iterdir() if file.is_file()]
    destination_path = Path(destination_folder)
    destination_files = {file.stem for file in destination_path.iterdir() if file.is_file()}
    
    for path in video_files:
        if destination_files.__contains__(path.stem):
            print(f'Skip {path.name}')
        else:
            options = {
                "OriginVideoPath": video_folder,
                "VideoSpeed": 0.9,
                "OverlayFilePath": 'D:/TIKTOK/OVERLAY.jpg',
                "Opacity": 5,
                "LogoFilePath": 'D:/TIKTOK/CIRCLE-LOGO.png',
                "LogoScale": 25, #tỷ lệ phần trăm
                "LogoLocationX": 100,
                "LogoLocationY": 250,
                "EditedVideoPath": destination_folder
            }

            edit_video(path.name, options)

channelCode = '@StarryriverAnime'
run_edit_video(f'D:/TIKTOK/YOUTUBE/{channelCode}', f'D:/TIKTOK/YOUTUBE/{channelCode}/EDITED')
#run_edit_video(f'D:\TIKTOK\DOUYIN\{channelCode}', f'D:\TIKTOK\DOUYIN\{channelCode}\EDITED')