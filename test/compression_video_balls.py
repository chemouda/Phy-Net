import math

import numpy as np
import tensorflow as tf
import cv2

import sys
sys.path.append('../')

import model.ring_net as ring_net
import model.unwrap_helper_test as unwrap_helper_test 
import random
import time

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('eval_dir', '../checkpoints/ring_net_eval_store',
                           """Directory where to write event logs.""")
tf.app.flags.DEFINE_string('checkpoint_dir', '../checkpoints/train_store_',
                           """Directory where to read model checkpoints.""")

def evaluate():
  FLAGS.system = "balls"
  FLAGS.model = "lstm_32x32x3"
  FLAGS.train = False 
  """ Eval the system"""
  with tf.Graph().as_default():
    # make inputs
    state_start = ring_net.inputs(1, 5) 

    # first step
    x_2, hidden_state = ring_net.encode_compress_decode(state_start[:,0,:,:,:], None, 1.0, 1.0)
    tf.get_variable_scope().reuse_variables()
    # unroll for 9 more steps
    for i in xrange(3):
      x_2, hidden_state = ring_net.encode_compress_decode(state_start[:,i+1,:,:,:], hidden_state, 1.0, 1.0)
    y_1 = ring_net.encoding(state_start[:,4,:,:,:], 1.0)
    y_2, hidden_state = ring_net.lstm_compression(y_1, hidden_state, 1.0)

    # rename output_t
    y_1 = y_2
    hidden_state_1 = hidden_state
    y_2, hidden_state_2 = ring_net.lstm_compression(y_1, hidden_state_1, 1.0)
    x_2 = ring_net.decoding(y_2)

    # restore network
    variables_to_restore = tf.all_variables()
    saver = tf.train.Saver(variables_to_restore)
    sess = tf.Session()
    ckpt = tf.train.get_checkpoint_state(FLAGS.checkpoint_dir)
    if ckpt and ckpt.model_checkpoint_path:
      saver.restore(sess, ckpt.model_checkpoint_path)
      print("restored file from " + ckpt.model_checkpoint_path)
    else:
      print("no chekcpoint file found from " + FLAGS.checkpoint_dir + FLAGS.model + FLAGS.atari_game + ", this is an error")

    # get frame
    tf.train.start_queue_runners(sess=sess)
    y_2_g, hidden_2_g = sess.run([y_1, hidden_state_1], feed_dict={})

    # Play!!!! 
    for step in xrange(10000):
      print(step)
      #time.sleep(.5)
      # calc generated frame from t
      x_2_g, y_2_g, hidden_2_g = sess.run([x_2, y_2, hidden_state_2],feed_dict={y_1:y_2_g, hidden_state_1:hidden_2_g})
      frame = np.uint8(np.minimum(np.maximum(0, x_2_g*255.0), 255))
      frame = frame[0, :, :, :]
      frame = cv2.resize(frame, (500, 500))
      cv2.imshow('frame', frame)
      cv2.waitKey(0)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.destroyAllWindows()

       
def main(argv=None):  # pylint: disable=unused-argument
  if tf.gfile.Exists(FLAGS.eval_dir):
    tf.gfile.DeleteRecursively(FLAGS.eval_dir)
  tf.gfile.MakeDirs(FLAGS.eval_dir)
  evaluate()


if __name__ == '__main__':
  tf.app.run()
