#thumbs.py - functions to work with thumbnails pulled from link pages

from PIL import Image

def youtube_stamp(original_thumb):
    background = Image.open(original_thumb)

    button = Image.open("youtube_button.png")

    # get the alpha-channel (used for non-replacement)
    background = background.convert("RGBA")
    r,g,b,a = button.split()
    # paste the button without replacing the alpha button of the button image
    background.paste(button, mask=a)

    background.save(original_thumb)

def vimeo_stamp(original_thumb):
    background = Image.open(original_thumb)

    button = Image.open("vimeo_button.png")

    # get the alpha-channel (used for non-replacement)
    background = background.convert("RGBA")
    r,g,b,a = button.split()
    # paste the button without replacing the alpha button of the button image
    background.paste(button, mask=a)

    background.save(original_thumb) 
