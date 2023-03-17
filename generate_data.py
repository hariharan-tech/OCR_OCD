import string
import os
from PIL import ImageFont, ImageDraw, Image, ImageChops
from numpy import sum as np_sum
from progress.bar import Bar
from project_config import CHARACTERS as characters, IMAGE_SIZE as img_size

def get_fonts_list():
    '''
        - Walks throughout the fonts-main directory to save the location of every tff file
        - Stores it in generator.txt
    '''
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
    '''
        - Creates folders to save the dataset (if not present)
    '''
    characters = list(string.ascii_letters+string.digits)
    for i in characters:
        if i in string.ascii_lowercase:
            os.makedirs(f".\dataset\{i}_L")
        elif i in string.ascii_uppercase:
            os.makedirs(f".\dataset\{i}_U")            
        else:
            os.makedirs(f".\dataset\{i}")

def predict_font_size(font_path,character):
    '''
        - Adaptively predicts the font size of image for a given fontstyle for each character
        - Returns the best possible fontsize as integer
    '''
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


def diff(img1,img2):
    ''' 
        Returns true if the given 2 images are same
        else returns false
    '''
    if abs(np_sum(ImageChops.difference(img1,img2)))==0: return True
    else: return False

def generate_image():
    '''
        Gets the list of available fonts from the text file generator.txt

        Loads each fontstyle, and for each character does the following:
            - For a alphabet character it creates the upper and lower case version
              at the appropriate font size using the predict_font_size function

            - Uses diff function (to check the difference) to check the difference 
              between the 2 images
            
            - If the images are different then it most probably means the fontstyle for 
              lower and uppercase characters are different, hence saves the images in both directories
              Else only saves it in the upper_case characters folder
            
            - For every number, generate the image and store it in corresponding directory
    '''
    global characters
    f = open("generator.txt","r")
    fonts = f.read().split("\n")[:-1]
    f.close()
    val = 1
    with Bar("Generating...",max=len(fonts)) as bar:
        for font in fonts:
            try:
                # accessing font name from font be like:
                # font_name = (font.split("\\")[-1]).split(".ttf")[0]

                for i in characters:
                    if i in string.ascii_uppercase:
                        font_used = ImageFont.truetype(font,predict_font_size(font,i))
                        img1u = Image.new(mode='RGB',size=img_size,color="#FFFFFF")
                        draw = ImageDraw.Draw(im=img1u)
                        draw.text((0,0),i,font=font_used,fill="black")
                        img2l = Image.new(mode='RGB',size=img_size,color="#FFFFFF")
                        draw = ImageDraw.Draw(im=img2l)
                        draw.text((0,0),i.lower(),font=font_used,fill="black")
                        if diff(img1u,img2l):
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
print("Loaded the fonts!")

# Run this to make directories
make_char_dirs()
print("Created Dataset directory and required internal subdirectories!")

# Run this to generate images
generate_image()

# Testing font size prediction testing
# for i in characters:
#     print(predict_font_size(r".\fonts-main\ufl\ubuntumono\UbuntuMono-Regular.ttf",i))