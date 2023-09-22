import subprocess,os,cleanup,threading

def download(file, filename):
    # Define the paths    
    current_dir = os.getcwd()
    input_audio_path = os.path.join(current_dir, "tmp", filename)
    if os.path.exists(input_audio_path):
        print("file already exist")
        return
    file.download(filename="tmp/"+filename)
    print("M4A  download completed successfully.")