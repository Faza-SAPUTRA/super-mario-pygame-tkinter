from PIL import Image

import customtkinter as ctk


class UiAssets:
    """Loads reusable pixel-art images for the CustomTkinter companion windows."""

    def __init__(self):
        self.titleLogo = self.loadImage("./img/title_screen.png", (2, 60, 176, 88), (220, 110), (255, 0, 220))
        self.mario = self.loadImage("./img/characters.gif", (276, 44, 292, 60), (64, 64))
        self.mushroom = self.loadImage("./img/Items.png", (0, 16, 16, 32), (48, 48))
        self.coin = self.loadImage("./img/Items.png", (0, 112, 16, 128), (42, 42))

    def loadImage(self, path, cropArea, size, transparentColor=None):
        image = Image.open(path).convert("RGBA")
        image = image.crop(cropArea)

        if transparentColor is not None:
            pixels = []

            for red, green, blue, alpha in image.getdata():
                if (red, green, blue) == transparentColor:
                    pixels.append((red, green, blue, 0))
                else:
                    pixels.append((red, green, blue, alpha))

            image.putdata(pixels)

        image = image.resize(size, Image.Resampling.NEAREST)
        return ctk.CTkImage(light_image=image, dark_image=image, size=size)
