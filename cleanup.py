import time,os

def performCleanup(filename):
    print("File will be deleted after 10 minutes")
    time.sleep(600)
    os.remove(filename)