import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


mnist = input_data.read_data_sets('MNIST-data', one_hot=True)
sess = tf.Session()

x = tf.placeholder(tf.float32, shape=[None, 784], name='input')
y_ = tf.placeholder(tf.float32, shape=[None, 10], name='label')

W = tf.Variable(tf.zeros([784, 10]), name='weight')
b = tf.Variable(tf.zeros([10]), name='bias')
y = tf.add(tf.matmul(x, W), b, name='prob')

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y_, logits=y))

tf.contrib.quantize.create_training_graph()

sess.run(tf.global_variables_initializer())
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

for _ in range(1000):
    batch = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch[0], y_: batch[1]})

saver = tf.train.Saver()
saver.save(sess, './local.ckpt')

with open('train.pb', 'w') as f:
    g = tf.get_default_graph()
    f.write(str(g.as_graph_def()))