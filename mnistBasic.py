
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# Only log errors (to prevent unnecessary cluttering of the console)
tf.logging.set_verbosity(tf.logging.ERROR)

logpath = "./tfb_logs/"

# We use the TF helper function to pull down the data from the MNIST site
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# x is the placeholder for the 28 x 28 image data (the input)
# y_ is a 10 element vector, containing the predicted probability of each digit (0-9) class
# Define the weights and balances (always keep the dimensions in mind)
x = tf.placeholder(tf.float32, shape=[None, 784], name="x_placeholder")
y_ = tf.placeholder(tf.float32, shape=[None, 10], name="y_placeholder")

W = tf.Variable(tf.zeros([784, 10]), name="weights_variable")
b = tf.Variable(tf.zeros([10]), name="bias_variable")

# Define the activation function = the real y. Softmax suits well for classification
y = tf.nn.softmax(tf.matmul(x, W) + b, name="softmaxActivation")

# Loss is defined as cross entropy between the prediction and the real value
# Each training step in gradient descent we want to minimize the loss
loss = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits_v2(labels=y_, logits=y, name="lossFunction")
)
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(loss, name="gradDescent")

# Initialize all variables
# Create an interactive session that can span multiple code blocks.
# Perform the initialization which is only the initialization of all global variables
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

# TensorBoard - Write the default graph out so we can view it's structure
tbWriter = tf.summary.FileWriter(logpath, sess.graph)

# Perform 1000 training steps
for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)  # get 100 random data points
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

# Evaluate how well the model did. Do this by compating the digit with the highest probability in
# actual (y) and predicted (y_)
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
test_accuracy = sess.run(
    accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}
)
print("Test Accuracy: {0}%".format(test_accuracy * 100.0))

sess.close()
