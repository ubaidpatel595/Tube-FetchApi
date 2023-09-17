from pytube import YouTube
import math,random,threading,time,downloadAudio
from flask import jsonify

def generateiD():
    userid = random.randint(0, 9999)
    return userid

def inactiveUser(id,users):
    print("Userid will be removed after 5 minutes")
    time.sleep(300)
    users.pop(id)
    print("Userid removed")

def info(link,users):
    if link != None and users != None :
        try:
            yt = YouTube(link)
            options = []
            for stream in yt.streams.filter(progressive=False):
                if stream.mime_type == "video/mp4":
                    options.append({
                        "itag": stream.itag,
                        "type": stream.type,
                        "quality": stream.resolution,
                        "size": math.ceil(stream.filesize / 1024 / 1024),
                    })
                elif stream.mime_type == "audio/mp4":
                    options.append({
                        "itag": stream.itag,
                        "type": stream.type,
                        "quality": stream.abr,
                        "size": math.ceil(stream.filesize / 1024 / 1024),
                    })

            unique = False
            id = 0
            while not unique:
                tid = generateiD()
                if tid in users:
                    print("user already exists")
                else:
                    threading.Thread(target=inactiveUser, args=[tid,users]).start()
                    users[tid] = [yt]
                    id = tid
                    unique = True
            
            audio = yt.streams.filter(only_audio=True, file_extension="mp4", bitrate="128kbps").first()
            fname = audio.default_filename.encode("ascii", "ignore").decode("ascii").replace(".mp4", ".m4a")
            thread = threading.Thread(target=downloadAudio.download, args=[audio, fname])
            thread.start()
            users[id].append(thread)
            response = {"thumbnail": yt.thumbnail_url, "title": yt.title, "options": options, "id": id}
            return jsonify(response),200
        except Exception as e:
            return jsonify({"message":str(e.__traceback__)}),500
    else:
     return jsonify({"message":'Invalid Link'}),406