import subprocess,os,cleanup,threading

def download(file, filename):
    # Define the paths    
    current_dir = os.getcwd()
    input_audio_path = os.path.join(current_dir, "tmp", filename)
    if os.path.exists(input_audio_path):
        print("audio file already exist")
        return
    file.download(filename="tmp/"+filename)

    # Specify the FFmpeg executable path
    ffmpeg_path = ""

    try:
        cmd = [
            os.environ.get("FFMPEG"),
            "-i", input_audio_path,
            "-acodec", "libmp3lame",
            "-q:a", "2",
            output_audio_path
        ]
        subprocess.run(cmd, check=True)
        print("M4A to MP3 conversion completed successfully.")
        os.remove(input_audio_path)  # Clean up: remove the temporary M4A file
        threading.Thread(target=cleanup.performCleanup,args=[output_audio_path]).start()
    except subprocess.CalledProcessError as e:
        print("Error converting M4A to MP3:", e)
