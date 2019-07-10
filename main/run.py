#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Evaluates a trained network."""

import argparse
import cv2
import logging
import numpy as np
import os
import re
import setproctitle
import skimage
import skimage.io
import skimage.transform
import sys
import time
import tensorflow as tf

import main.models as models
import main.utils as utils


logging.basicConfig(format="[%(process)d] %(levelname)s %(filename)s:%(lineno)s | %(message)s")
log = logging.getLogger("train")
log.setLevel(logging.INFO)

os.environ["CUDA_VISIBLE_DEVICES"]="1"
def get_input_list(path):
  regex = re.compile(".*.(png|jpeg|jpg|tif|tiff)")
  if os.path.isdir(path):
    inputs = os.listdir(path)
    inputs = [os.path.join(path, f) for f in inputs if regex.match(f)]
    log.info("Directory input {}, with {} images".format(path, len(inputs)))

  elif os.path.splitext(path)[-1] == ".txt":
    dirname = os.path.dirname(path)
    with open(path, 'r') as fid:
      inputs = [l.strip() for l in fid.readlines()]
    inputs = [os.path.join(dirname, 'input', im) for im in inputs]
    log.info("Filelist input {}, with {} images".format(path, len(inputs)))
  elif regex.match(path):
    inputs = [path]
    log.info("Single input {}".format(path))
  return inputs


def main(args):
  setproctitle.setproctitle('DeepUPE')

  inputs = get_input_list(args.input)

  # -------- Load params ----------------------------------------------------
  config = tf.ConfigProto()
  config.gpu_options.allow_growth = True
  with tf.Session(config=config) as sess:
    checkpoint_path = tf.train.latest_checkpoint(args.checkpoint_dir)
    if checkpoint_path is None:
      log.error('Could not find a checkpoint in {}'.format(args.checkpoint_dir))
      return

    metapath = ".".join([checkpoint_path, "meta"])
    log.info('Loading graph from {}'.format(metapath))
    tf.train.import_meta_graph(metapath)

    model_params = utils.get_model_params(sess)

  # -------- Setup graph ----------------------------------------------------
  if not hasattr(models, model_params['model_name']):
    log.error("Model {} does not exist".format(params.model_name))
    return
  mdl = getattr(models, model_params['model_name'])

  tf.reset_default_graph()
  net_shape = model_params['net_input_size']
  t_fullres_input = tf.placeholder(tf.float32, (1, None, None, 3))
  t_lowres_input = tf.placeholder(tf.float32, (1, net_shape, net_shape, 3))

  with tf.variable_scope('inference'):
    prediction = mdl.inference(
        t_lowres_input, t_fullres_input, model_params, is_training=False)
  output = tf.cast(255.0*tf.squeeze(tf.clip_by_value(prediction, 0, 1)), tf.uint8)
  saver = tf.train.Saver()


  with tf.Session(config=config) as sess:
    log.info('Restoring weights from {}'.format(checkpoint_path))
    saver.restore(sess, checkpoint_path)

    for idx, input_path in enumerate(inputs):

      log.info("Processing {}".format(input_path))
      im_input = cv2.imread(input_path, -1)  # -1 means read as is, no conversions.
      if im_input.shape[2] == 4:
        log.info("Input {} has 4 channels, dropping alpha".format(input_path))
        im_input = im_input[:, :, :3]

      im_input = np.flip(im_input, 2)  # OpenCV reads BGR, convert back to RGB.



      im_input = skimage.img_as_float(im_input)

      lowres_input = skimage.transform.resize(
          im_input, [net_shape, net_shape], order = 0)


      fname = os.path.splitext(os.path.basename(input_path))[0]
      output_path = os.path.join(args.output, fname+".png")
      basedir = os.path.dirname(output_path)

      im_input = im_input[np.newaxis, :, :, :]
      lowres_input = lowres_input[np.newaxis, :, :, :]

      feed_dict = {
          t_fullres_input: im_input,
          t_lowres_input: lowres_input
      }

      out_ =  sess.run(output, feed_dict=feed_dict)

      if not os.path.exists(basedir):
        os.makedirs(basedir)
      

      out_ =  (out_/255.0)**1.0
      out_ = np.clip(out_, im_input, 1)
      
      final_result = np.divide(im_input.astype(np.float), out_.astype(np.float))
     
      skimage.io.imsave(output_path, final_result)




if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('checkpoint_dir', default=None, help='path to the saved model variables')
  parser.add_argument('input', default=None, help='path to the validation data')
  parser.add_argument('output', default=None, help='path to save the processed images')
  args = parser.parse_args()
  main(args)
