from __future__ import print_function
import PIL
import numpy as np
import tensorflow as tf

model_fn = '/tmp/retrain_arch_mobilenet_1.0_128/model/mobilenet_v1_1.0_128_frozen.pb'

# creating TensorFlow session and loading the model
graph = tf.Graph()
sess = tf.InteractiveSession(graph=graph)
with tf.gfile.FastGFile(model_fn, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
t_input = tf.placeholder(np.float32, name='input') # define the input tensor
imagenet_mean = 127
t_preprocessed = tf.expand_dims((t_input-imagenet_mean)/32, 0)
tf.import_graph_def(graph_def, {'input':t_preprocessed})

ops=graph.get_operations()
# Picking some internal layer. Note that we use outputs before applying the ReLU nonlinearity
# to have non-zero gradients for features with negative initial activations.
layer = 'MobilenetV1/MobilenetV1/Conv2d_10_pointwise/Conv2D'
channel = 2 # picking some feature channel to visualize

# start with a gray image with a little noise
img_noise = np.random.uniform(size=(128,128,3)) + 100.0

   
def visstd(a, s=0.1):
    '''Normalize the image range for visualization'''
    return (a-a.mean())/max(a.std(), 1e-4)*s + 0.5

def T(layer):
    '''Helper for getting layer output tensor'''
    return graph.get_tensor_by_name("import/%s:0"%layer)

def render_naive(t_obj, img0=img_noise, iter_n=1000, step=1):
    t_score = tf.reduce_mean(t_obj) # defining the optimization objective
    t_grad = tf.gradients(t_score, t_input)[0] # behold the power of automatic differentiation!
    
    img = img0.copy()
    for i in range(iter_n):
        g, score = sess.run([t_grad, t_score], {t_input:img})
        # normalizing the gradient, so the same step size should work 
        g /= g.std()+1e-8         # for different layers and networks
        img += g*step
        print(score)
    a = visstd(img)
    a = np.uint8(np.clip(a, 0, 1)*255)
    PIL.Image.fromarray(a).save('test.png')

render_naive(T(layer)[:,:,:,channel])
