import string
import os
from PIL import ImageFont, ImageDraw, Image
from project_config import CHARACTERS as characters, IMAGE_SIZE as img_size

# path = os.getcwd()+"fonts-main\\"

# characters = list(string.ascii_uppercase+string.ascii_lowercase+string.digits)
# img_size = (40,60)

def get_fonts_list():
    f = open("generator.txt","w")
    path = ".\\fonts-main"
    for root, dirs, files in os.walk(path):
        for file in files:
            if ".ttf" in file:
                # print(f"{root}\{file}")
                f.write(f"{root}\{file}\n")
    f.close()

# make sure this isn't run when folders already exists
def make_char_dirs():
    global characters
    for i in characters:
        if i in string.ascii_lowercase:
            os.makedirs(f".\dataset_new\{i}L")
        elif i in string.ascii_uppercase:
            os.makedirs(f".\dataset_new\{i}H")            
        else:
            os.makedirs(f".\dataset_new\{i}")

def predict_font_size(font_path,character):
    global img_size
    font_size = min(img_size)//3
    font = ImageFont.truetype(font_path,font_size)
    # print("test")
    # changed the deprecating function
    while font.getbbox(character)[2] < img_size[0] and font.getbbox(character)[3] < img_size[1]:
        font_size+=3
        font = ImageFont.truetype(font_path,font_size)

    # print(font.getsize(character))
    # DeprecationWarning: getsize is deprecated and will be removed in Pillow 10 (2023-07-01). Use getbbox or getlength instead.
    # use this instead getbbox(character)
    # print(font.getbbox(character))

    # Testing the Working
    # font = ImageFont.truetype(font_path,font_size-1)
    # img = Image.new(mode="RGB",size=img_size,color="white")
    # draw = ImageDraw.Draw(im=img)
    # draw.text((0,0),character,font=font,fill="black")
    # img.save(f"./test/{character}.png")
    return font_size-3

def generate_image():
    global characters
    f = open("generator.txt","r")
    fonts = f.read().split("\n")[:-1]
    f.close()
    for font in fonts[:20]:
        # accessing font name from font be like:
        # print((font.split("\\")[-1]).split(".ttf")[0])
        font_name = (font.split("\\")[-1]).split(".ttf")[0]

        for i in characters:
            font_used = ImageFont.truetype(font,predict_font_size(font,i))
            image = Image.new(mode='RGB',size=img_size,color="#FFFFFF")
            draw = ImageDraw.Draw(im=image)
            draw.text((0,0),i,font=font_used,fill="black")
            if i in string.ascii_lowercase:
                image.save(f"dataset_new/{i}L/{font_name}.png")
            elif i in string.ascii_uppercase:
                image.save(f"dataset_new/{i}H/{font_name}.png")
            else:
                image.save(f"dataset_new/{i}/{font_name}.png")

# Run this to generate the fonts available
# get_fonts_list()

# Run this to make directories
# make_char_dirs()

# Run this to generate images
generate_image()

# Testing font size prediction 
# for i in characters:
#     print(predict_font_size(r".\fonts-main\ufl\ubuntumono\UbuntuMono-Regular.ttf",i))