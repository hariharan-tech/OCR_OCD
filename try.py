import string
# import pytesseract
from PIL import ImageFont, ImageDraw, Image

path = "D:\SSN ECE\sem6\ml_lab\mini_project_ML\\fonts-main\ofl\creepster\Creepster-Regular.ttf"

font = ImageFont.truetype(path,50)

characters = list(string.ascii_lowercase+string.ascii_uppercase+string.digits)
print(characters)

for i in characters:
    image = Image.new(mode='RGB', size=(50,50),color="#FFFFFF")
    draw = ImageDraw.Draw(im=image)
    draw.text((0,0),i,font=font,fill="black")
    image.save("fonts-name/"+str(i)+".png")
# image.show()
# print(pytesseract.image_to_string(Image.open('fonts-name/a.png')))