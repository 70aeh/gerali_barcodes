from barcode import EAN13_GUARD
from barcode.writer import ImageWriter
# from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

out_dir = 'out'

bar_text = 'Jacheta Women\'s Aviator, Negru, 42' # Text
bar_text_1 = 'Jacheta Women\'s Aviator' # Text
bar_text_2 = 'Negru, 42' # Text
# bar_text = 'Jacheta Test1234567890|1234567890|1234567890' # Text
bar_code = '5949286308040' # EAN13

text_font_size = 25

# print to a file-like object:
# rv = BytesIO()
# img = EAN13_GUARD(bar_code, writer=ImageWriter()).write(rv)

# or sure, to an actual file:
def generate_code(bar_code, bar_text, save_file):
    save_path = 'tmp.jpeg'

    with open(save_path, 'wb') as f:
        EAN13_GUARD(bar_code, writer=ImageWriter()).write(f)

    img_barcode = Image.open(save_path)

    img_text = Image.new('RGB', (img_barcode.size[0], 80), color=(255, 255, 255))

    # fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', text_font_size)
    fnt = ImageFont.truetype('/Library/Fonts/Roboto-Medium.ttf', text_font_size)

    d = ImageDraw.Draw(img_text)
    d.text((75, 40), bar_text, font=fnt, fill=(0, 0, 0))
    # d.text((75, 20), bar_text_1, font=fnt, fill=(0, 0, 0))
    # d.text((75, 50), bar_text_2, font=fnt, fill=(0, 0, 0))

    # img_text.save('pil_text_font.png')

    new_im = Image.new('RGB', (img_barcode.size[0], img_barcode.size[1]+img_text.size[1]))

    y_offset = 0
    for im in [img_text, img_barcode]:
      new_im.paste(im, (0, y_offset))
      y_offset += im.size[1]

    new_im.save(save_file, text='overlay text')


if __name__ == '__main__':
    generate_code(bar_code, bar_text, 'demo.png')

print('Done.')