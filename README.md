# Hoarder, a IIIF Image Cacher

Hoarder is a simple caching system with some tweaks to work with the Tuatara IIIF Image Server.  Put docker on your machine, clone it and build it.

```
git clone thisrepo
cd hoarder
docker build -t hoarder .
```

Then run the container at a port of your choosing (in this case 8888) to serve a directory of images of your choosing (in this case /var/www/hoarder/app/files)

```docker run -v /var/www/hoarder/app/files:/app/files -p 8888:80 hoarder:latest```
