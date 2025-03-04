# Noticeboard-2

Noticeboard? No I didn't see any planks

# This is a board for notices

You can see it in studio red or noticeboard.ury.org.uk

It uses the myradio api to dynamically update open positions and upcoming events and also to recommend some of our shows.

It also has a CMS webpage thing where you can edit the rest of the page.

# How do I use it?

go to noticeboard.ury.org.uk and put it on your screen its not hard

if you are a comp officer or have the edit banner permission then you can also use noticeboard.ury.org.uk/edit to update it

# Development

To develop this you will need docker. You might not technically need docker but you should use it anyway. its useful and looks good on your CV.

To run the project, first clone the repo onto your device,

Then copy `.env.example` to `.env` and fill in your MyRadio API Key (If you don't already have one harrass the Head of Computing.),

Then, run:

```
docker compose up -d

```

(The -d flag will run the container in the background, omit it if you wish to run the container in the foreground)


There you go! you can now view your own beautiful noticeboard at localhost:5042
Neat!

#credits

thank you Jamies Parker-East for helping to take the cool background images
