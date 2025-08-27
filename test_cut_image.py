import cut_image as ci
from PIL import Image

img = Image.open("sample.png")
print("画像の型:", type(img))
cropped = ci.select_and_crop(img)
print("切り抜き結果の型:", type(cropped))
if cropped is not None:
    cropped.save("cropped.png", format="PNG")