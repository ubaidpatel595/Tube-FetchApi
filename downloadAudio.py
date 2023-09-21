import subprocess,os,cleanup,threading
from dotenv import load_dotenv
load_dotenv()

def download(file, filename):
    # Define the paths    
    current_dir = os.getcwd()
    input_audio_path = os.path.join(current_dir, "tmp", filename)
    if os.path.exists(input_audio_path):
        print("audio file already exist")
        return
    file.download(filename="tmp/"+filename)
    print("Audio Downloaded successfully")
    threading.Thread(target=cleanup.performCleanup,args=[input_audio_path]).start()