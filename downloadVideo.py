import os,threading,cleanup,subprocess

def download(file, fname,itag):
    # Define the paths 
    current_dir = os.getcwd()
    input_video_path = os.path.join(current_dir, "tmp", "1" + fname)
    input_audio_path = os.path.join(current_dir, "tmp", fname.replace(".mp4",".mp3"))
    output_video_path = os.path.join(current_dir, "tmp", fname.replace(".mp4",str(itag)+".mp4"))
    if os.path.exists(output_video_path):
                print("File already exist")
                return
    file.download(filename = "tmp/1" + fname)
    # Specify the FFmpeg executable path
    ffmpeg_path = "C:/Users/UBAID PATEL/Downloads/ffmpeg-2023-09-07-git-9c9f48e7f2-full_build/ffmpeg-2023-09-07-git-9c9f48e7f2-full_build/bin/ffmpeg.exe"

    try:
        cmd = [
            ffmpeg_path,
            "-i", input_video_path,
            "-i", input_audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-strict", "experimental",
            output_video_path
        ]
        subprocess.run(cmd, check=True)
        # Clean up: remove the temporary audio and video files
        os.remove(input_audio_path)
        os.remove(input_video_path)
        threading.Thread(target=cleanup.performCleanup,args=[output_video_path]).start()
        print("Audio and video merging completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error merging audio and video:", e)
