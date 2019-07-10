

import tensorflow as tf

import numpy as np
from scipy.integrate import odeint

def l2_loss(target, prediction, name=None):
  with tf.name_scope(name, default_name='l2_loss', values=[target, prediction]):
    loss = tf.reduce_mean(tf.square(target-prediction))
  return loss

def tv_loss(input_, output, weight):
    I = tf.image.rgb_to_grayscale(input_)
    L = tf.log(I+0.0001)
    dx = L[:, :-1, :-1, :] - L[:, :-1, 1:, :]
    dy = L[:, :-1, :-1, :] - L[:, 1:, :-1, :]

    alpha = tf.constant(1.2)
    lamda = tf.constant(1.5)  
    dx = tf.divide(lamda, tf.pow(tf.abs(dx),alpha)+ tf.constant(0.0001))
    dy = tf.divide(lamda, tf.pow(tf.abs(dy),alpha)+ tf.constant(0.0001))
    shape = output.get_shape()
    x_loss = dx *((output[:, :-1, :-1, :] - output[:, :-1, 1:, :])**2)
    y_loss = dy *((output[:, :-1, :-1, :] - output[:, 1:, :-1, :])**2)
    tvloss = tf.reduce_mean(x_loss + y_loss)/2.0
    return tvloss*weight

