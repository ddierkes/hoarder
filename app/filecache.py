import os, shutil, errno
import requests

basepath = "https://images.mohistory.org/IIIF/webimages/Mohistory.org/Homepages/"
def main(path):
    r = requests.get(basepath+path, stream=True)
    if r.status_code == 200:
        filename = path.split('/')[-1]
        justdirs = path[:-(len(filename)+1)]
        try:
            os.makedirs('files/'+justdirs)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir('files/'+justdirs):
                pass
        with open('files/'+path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)



if __name__ == "__main__":
    main("mhs-rebranding.jpg/square/1920,/0/default.jpg")
    main("mhs-rebranding.jpg/info.json")
