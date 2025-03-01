# Noticeboard-2

Noticeboard? No I didn't see any planks

# This is a board for notices

You can see it in studio red or noticeboard.ury.org.uk

It uses the myradio api to dynamically update open positions and upcoming events and also to recommend some of our shows.

It also has a backend webpage thing where you can edit the rest of the page.

# How do I use it?

go to noticeboard.ury.org.uk and put it on your screen its not hard

if you are a comp officer or have the edit banner permission then you can also use noticeboard.ury.org.uk/edit to update it

# Development

To develop this you will need docker. You might not technically need docker but you should use it anyway. its useful and looks good on your CV.

To build the project clone it onto your device and then run (you'll need to do this every time you modify the project)

```
docker build -t noticeboard .
```

then to run the project:

```
docker run -p 5042:5042 noticeboard
```

There you go! you can now view your own beautiful noticeboard at localhost:5042
Neat!

You will notice it doesn't look right and loads of it is broken. Thats because it can't authenticate the myradio api requests.
To make it do this you'll need a myradio api key. If you don't already have one harrass the head of computing.

Once you've obtained your api key you can set it as an env variable when you run your container:

```
docker run -p 5042:5042 -e MYRADIO_API_KEY='[your_api_key]' noticeboard
```

If you want some permanent storage of noticeboard content you'll need to use volumes.

First create a new volume:

```
docker volume create plankstore
```

then you can bind it when you run the container. For this app you want it bound to /opt/

```
docker run -p 5042:5042 -v plankstore:/opt/ noticeboard
```

and if you want it all at once

```
docker run -p 5042:5042 -v plankstore:/opt/ -e MYRADIO_API_KEY='[your_api_key]' noticeboard
```
