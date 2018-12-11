# Hoarder, a IIIF Image Cacher

Hoarder is a simple caching system with some tweaks to work with the Tuatara IIIF Image Server.  Put docker on your machine, clone it and build it.

```
git clone thisrepo
cd hoarder
docker build -t hoarder .
```

Then run the container at a port of your choosing (in this case 8888) to serve a directory of images of your choosing (in this case /var/www/hoarder/app/files)

```docker run -v /var/www/hoarder/app/files:/app/files -p 9999:80 hoarder:latest```

The cache will fill up very quickly when used with tools like openseadragon which require a great many derivative files.  A utility script is included at app/cleanup.py which can be run as a cron job.  it takes arguments for the file directory, the size you wish to keep your cache at, a 'test' or 'run' value for determining if you intend to see what needs deleted or to actually delete them, and finally a number of days from today to purge.  The script can be run like so.

```python3 cleanup.py 'files' 2000000 'test' 20```
