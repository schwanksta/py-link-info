from PIL import Image
# the image we want to start with
background = Image.open("default.jpg")
# the button, which gets masked over our background
button = Image.open("playbutton.png")
# get the alpha-channel (used for non-replacement)
background = background.convert("RGBA")
r,g,b,a = button.split()
# paste the frame button without replacing the alpha button of the button image
background.paste(button, mask=a)
background.save("thumb_generated.png")

