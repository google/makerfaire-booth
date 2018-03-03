from PIL import Image
from burger_data import BurgerElement, burger_asset

def render_burger(burger):
  icon = Image.new("RGB",(64, 64), (255, 255, 255))

  images = {}
  size = 0
  for element in burger:
    asset = burger_asset[element]
    size += asset.size[1]
  height = (64 - size)/2

  for element in burger:
    asset = burger_asset[element]
    width = (64 - asset.size[0]) / 2
    icon.paste(asset, (width, height))
    height += asset.size[1]

  return icon
