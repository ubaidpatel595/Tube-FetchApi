from flask import Flask,send_file,make_response,render_template
from pytube import YouTube,Stream
import math
from flask import request
from moviepy.editor import VideoFileClip, AudioFileClip
import os,time,threading
from flask_cors import CORS
def performCleanup(file,t):
    time.sleep(t)
    os.remove(file)


app = Flask("Yt Downloader")
CORS(app,supports_credentials=True,resources={r"/*": {"origins":"*"}},allow_headers=['*','Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, filename'])
@app.route("/")
def home():
   return render_template("index.html")

@app.route("/info",methods=["POST"])
def info():
    print(request.get_json()["link"])
    yt = YouTube(request.get_json()["link"])  
    options = []  
    
    for stream in yt.streams.filter(progressive=False):
     if(stream.mime_type == "video/mp4"):
       options.insert(len(options),{"itag":stream.itag,"type":stream.type,"quality":stream.resolution,"size":math.ceil(stream.filesize / 1024 / 1024)})
     elif(stream.mime_type == "audio/mp4"):
       options.insert(len(options),{"itag":stream.itag,"type":stream.type,"quality":stream.abr,"size":math.ceil(stream.filesize / 1024 / 1024)})
       
    response = {"thumbnail":yt.thumbnail_url,"title":yt.title,"options":options}
    return response
    
@app.route("/download",methods=['POST'])
def download():  
    yt = YouTube(request.get_json()["link"])  
    file = yt.streams.get_by_itag(request.get_json()["itag"])
    headers = {
        'Content-Disposition': f'attachment; filename={file.default_filename.split("/")[-1]}',
        'Content-Type': 'application/octet-stream',
        'filename':file.default_filename
         }
    if file.mime_type == "video/mp4":
       fname = file.default_filename.encode('ascii', 'ignore').decode('ascii')
       file.download(filename="1"+fname)
       audio = yt.streams.filter(only_audio=True,file_extension="mp4",bitrate="128kbps").first()
       audio.download(filename=fname.replace(".mp4",".m4a"))
       video_clip = VideoFileClip(filename="1"+fname)  # Load the video
       audio_clip = AudioFileClip(filename=fname.replace(".mp4",".m4a"))

       # Ensure the audio duration matches the video duration
       if audio_clip.duration > video_clip.duration:
           audio_clip = audio_clip.subclip(0, video_clip.duration)

       # Set the audio of the video clip to the audio clip
       video_clip = video_clip.set_audio(audio_clip)

       # Specify the frame rate here (e.g., 30 FPS)
       video_clip = video_clip.set_duration(video_clip.duration)

       # Write the merged video to an output file
       video_clip.write_videofile(fname)
       print("Video Converted")
       os.remove(fname.replace(".mp4",".m4a"))
       os.remove("1"+fname)
       threading.Thread(target=performCleanup,args=(fname,300)).start()
    else:
        filename = file.default_filename.replace(".mp4",".m4a").encode('ascii', 'ignore').decode('ascii')
        file.download(filename=filename)
        audio_clip = AudioFileClip(filename)
        # Export the audio to MP3 format
        audio_clip.write_audiofile(filename.replace(".m4a",".mp3"), codec="mp3")
        os.remove(filename)
        
        print("Audio converted")
        headers['Content-Disposition'] = f'attachment; filename={filename.replace(".m4a",".mp3").split("/")[-1]}'
        headers['filename'] = filename.replace(".m4a",".mp3")
        threading.Thread(target=performCleanup,args=(filename.replace(".m4a",".mp3"),300)).start()
    
    response = make_response(send_file(headers['filename'], as_attachment=True, download_name=headers['filename']))
    response.headers = headers
    return response


@app.route("/t/<a>")
def test( ):
   return "a"
if __name__ == "__main__":
    app.run(debug=True,host='192.168.43.160',port=5000)

 