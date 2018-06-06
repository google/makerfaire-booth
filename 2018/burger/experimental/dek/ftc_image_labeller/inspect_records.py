from PIL import Image, ImageDraw, ImageFont
import io
import tensorflow as tf
fnt = ImageFont.truetype('LucidaSansRegular.ttf', 12)

flags = tf.app.flags
flags.DEFINE_string('records', 'records/train.records', 'Path to records to decode')
flags.DEFINE_string('decoded_dir', 'decoded', 'Path to write decoded records')
FLAGS = flags.FLAGS


example = tf.train.Example()
counter = 0
for record in tf.python_io.tf_record_iterator(FLAGS.records):
    example.ParseFromString(record)
    f = example.features.feature
    height = f['image/height'].int64_list.value[0]
    width = f['image/width'].int64_list.value[0]
    e = f['image/encoded'].bytes_list.value[0]

    im = Image.open(io.BytesIO(e))
    draw = ImageDraw.Draw(im)

    for i in range(len(f['image/object/class/text'].bytes_list.value)):
        class_text = f['image/object/class/text'].bytes_list.value[i]
        xmin = f['image/object/bbox/xmin'].float_list.value[i]
        ymin = f['image/object/bbox/ymin'].float_list.value[i]
        xmax = f['image/object/bbox/xmax'].float_list.value[i]
        ymax = f['image/object/bbox/ymax'].float_list.value[i]
        draw.rectangle([xmin*width, ymin*height, xmax*width, ymax*height], outline="rgb(255,0,0)")
        draw.text((xmin*width, ymin*height), class_text.decode('utf-8'), font=fnt, fill=(255,0,0,255))

    im.save(os.path.join(FLAGS.decoded_dir, "%05d.png" % counter)
    counter += 1
