from PIL import Image, ImageDraw, ImageFont
import io
import tensorflow as tf
fnt = ImageFont.truetype('LucidaSansRegular.ttf', 12)


example = tf.train.Example()
counter = 0
for record in tf.python_io.tf_record_iterator("eval.records"):
    example.ParseFromString(record)
    f = example.features.feature
    height = f['image/height'].int64_list.value[0]
    width = f['image/width'].int64_list.value[0]
    e = f['image/encoded'].bytes_list.value[0]
    
    im = Image.open(io.BytesIO(e))
    im.save("decoded/%05d.nobox.png" % counter)
    draw = ImageDraw.Draw(im)

    for i in range(len(f['image/object/class/text'].bytes_list.value)):
        class_text = f['image/object/class/text'].bytes_list.value[i]
        xmin = f['image/object/bbox/xmin'].float_list.value[i]
        ymin = f['image/object/bbox/ymin'].float_list.value[i]
        xmax = f['image/object/bbox/xmax'].float_list.value[i]
        ymax = f['image/object/bbox/ymax'].float_list.value[i]
        draw.rectangle([xmin*width, ymin*height, xmax*width, ymax*height], outline="rgb(255,0,0)")
        draw.text((xmin*width, ymin*height), class_text.decode('utf-8'), font=fnt, fill=(255,0,0,255))

    im.save("decoded/%05d.png" % counter)
    counter += 1
