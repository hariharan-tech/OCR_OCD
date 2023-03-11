import string
import os
from PIL import ImageFont, ImageDraw, Image, ImageChops
from numpy import sum as np_sum
from progress.bar import Bar
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
    characters = list(string.ascii_letters+string.digits)
    for i in characters:
        if i in string.ascii_lowercase:
            os.makedirs(f".\dataset\{i}_L")
        elif i in string.ascii_uppercase:
            os.makedirs(f".\dataset\{i}_U")            
        else:
            os.makedirs(f".\dataset\{i}")

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


# Get MSE between 2 images
def mse(img1,img2):
    # print(np_sum(ImageChops.difference(img1,img2)))
    if abs(np_sum(ImageChops.difference(img1,img2)))==0:
        return True
    else: return False

def generate_image():
    global characters
    f = open("generator.txt","r")
    fonts = f.read().split("\n")[:-1]
    f.close()
    val = 1
    with Bar("Generating...",max=len(fonts)) as bar:
        for font in fonts:
            # accessing font name from font be like:
            # print((font.split("\\")[-1]).split(".ttf")[0])
            try:
                font_name = (font.split("\\")[-1]).split(".ttf")[0]
                for i in characters:
                    if i in string.ascii_uppercase:
                        font_used = ImageFont.truetype(font,predict_font_size(font,i))
                        img1u = Image.new(mode='RGB',size=img_size,color="#FFFFFF")
                        draw = ImageDraw.Draw(im=img1u)
                        draw.text((0,0),i,font=font_used,fill="black")
                        img2l = Image.new(mode='RGB',size=img_size,color="#FFFFFF")
                        draw = ImageDraw.Draw(im=img2l)
                        draw.text((0,0),i.lower(),font=font_used,fill="black")
                        if mse(img1u,img2l):
                            img1u.save(f"dataset/{i.upper()}_U/{i.upper()}_U_{val}.png")
                        else:
                            img1u.save(f"dataset/{i}_U/{i}_U_{val}.png")
                            img2l.save(f"dataset/{i}_L/{i}_L_{val}.png")
                    else:
                        img = Image.new(mode='RGB',size=img_size,color="#FFFFFF")
                        draw = ImageDraw.Draw(im=img)
                        draw.text((0,0),i,font=font_used,fill="black")
                        img.save(f"dataset/{i}/{val}.png")
            except KeyboardInterrupt:
                print("exiting")
                exit(1)
            except:
                print("err")
                pass
            val+=1
            bar.next()
        

# Run this to generate the fonts available
# get_fonts_list()
print("Fonts vanthachu da!")

# Run this to make directories
make_char_dirs()
print("Dirs panniyachu da!")

# Run this to generate images
generate_image()

# Testing font size prediction 
# for i in characters:
#     print(predict_font_size(r".\fonts-main\ufl\ubuntumono\UbuntuMono-Regular.ttf",i))