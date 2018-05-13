from PIL import Image, ImageDraw
import io
import tensorflow as tf


example = tf.train.Example()
for record in tf.python_io.tf_record_iterator("../data/burgers_eval.record"):
    example.ParseFromString(record)
    f = example.features.feature
    height = f['image/height'].int64_list.value[0]
    width = f['image/width'].int64_list.value[0]
    class_text = f['image/object/class/text'].bytes_list.value[0]
    xmin = f['image/object/bbox/xmin'].float_list.value[0]
    ymin = f['image/object/bbox/ymin'].float_list.value[0]
    xmax = f['image/object/bbox/xmax'].float_list.value[0]
    ymax = f['image/object/bbox/ymax'].float_list.value[0]
    e = f['image/encoded'].bytes_list.value[0]
    i = Image.open(io.BytesIO(e))
    i.save("decoded/%s_%03d_%03d_%03d_%03d.nobox.png" % (class_text, int(round(xmin*width)), int(round(ymin*height)), int(round(xmax*width)), int(round(ymax*height))))
    
    draw = ImageDraw.Draw(i)
    draw.rectangle([xmin*width, ymin*height, xmax*width, ymax*height], outline="rgb(255,0,0)")
    i.save("decoded/%s_%03d_%03d_%03d_%03d.png" % (class_text, int(round(xmin*width)), int(round(ymin*height)), int(round(xmax*width)), int(round(ymax*height))))
