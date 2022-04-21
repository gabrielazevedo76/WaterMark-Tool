import os, sys
from PIL import Image, ImageEnhance

class WaterMark():
    def __init__(self, _img: str, _logo: str) -> None:
        self.img = _img
        self.logo = _logo
        self.widthImg, self.heightImg = Image.open(self.img).size[0], Image.open(self.img).size[1]

    # Resize logo (default value = (125, 125))
    def resize(self, opacity: float) -> None:
        f, e = os.path.splitext(self.logo)
        folderPath, imgName = f.split("/")[0], f.split("/")[1]

        try:
            with Image.open(self.logo) as im:
                if im.mode != "RGBA":
                    im = im.convert("RGBA")
                else:
                    im = im.copy()

                im = im.resize((125, 125))
                alpha = im.split()[3]
                alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
                im.putalpha(alpha)
                self.logo = im
                self.logo.save(f"images_resized/{imgName}_resized{e}")

                return im

        except OSError:
            print("cannot resize", self.logo)

    # Merge image choosed with the resized logo
    def merge(self, widthUser, heightUser) -> None:
        #widthUser = int(input(f"Choose a width between 0 and {(self.widthImg - 125)}: "))
        #heightUser = int(input(f"Choose a width between 0 and {self.heightImg}: "))
        if(widthUser > (self.widthImg - 125) or heightUser > self.heightImg):
            raise Exception("Width and Height have to be between the range given!")

        f,e = os.path.splitext(self.img)
        folderPath, imgName = f.split("/")[0], f.split("/")[1]

        try:
            with Image.open(self.img) as im, self.logo as logo:
                im.paste(logo, box=(widthUser, heightUser), mask=logo)
                im.save(f"images_watermarked/{imgName}_watermarked.png")

                return im
        except:
            print(f"cannot merge {self.img} with {self.logo}")
            
IMG = "images/calabresa.jpeg"
LOGO = "images/logo.png"

wm = WaterMark(IMG, LOGO)
wm.resize(0.4)
wm.merge(0, 0)


