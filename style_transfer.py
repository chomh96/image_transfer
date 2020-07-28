# -*- coding: utf-8 -*-
#
#@title Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# 결과 로그 상태 숨기기
import os
# 0 = all messages are logged (default behavior)
# 1 = INFO messages are not printed
# 2 = INFO and WARNING messages are not printed
# 3 = INFO, WARNING, and ERROR messages are not printed
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf

import numpy as np
import PIL.Image
import tensorflow_hub as hub
import sys

import Parser

def tensor_to_image(tensor):
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return PIL.Image.fromarray(tensor)

"""Download images and choose a style image and a content image:"""

# content_path = tf.keras.utils.get_file('YellowLabradorLooking_new.jpg', 'https://storage.googleapis.com/download.tensorflow.org/example_images/YellowLabradorLooking_new.jpg')
# style_path = tf.keras.utils.get_file('kandinsky5.jpg','https://storage.googleapis.com/download.tensorflow.org/example_images/Vassily_Kandinsky%2C_1913_-_Composition_7.jpg')
#
def load_img(path_to_img):
  max_dim = 512
  img = tf.io.read_file(path_to_img)
  img = tf.image.decode_image(img, channels=3)
  img = tf.image.convert_image_dtype(img, tf.float32)

  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  long_dim = max(shape)
  scale = max_dim / long_dim

  new_shape = tf.cast(shape * scale, tf.int32)

  img = tf.image.resize(img, new_shape)
  img = img[tf.newaxis, :]
  return img

option = Parser.parse_args();

# 이미지 경로 설정
try:
    content_image = load_img(option.content_img)
except Exception as e:
    print('Check content_image path')
    sys.exit(0)

try:
    style_image = load_img(option.style_img)
except Exception as e:
    print('Check style_image path')
    sys.exit(0)

# 세로, 가로 순서
if(option.resize_width):
    content_image = tf.image.resize(content_image, (option.resize_width, option.resize_width))
    style_image = tf.image.resize(style_image, (option.resize_width, option.resize_width))

# 모듈 경로 설정
hub_module = hub.load(option.module_path) # Default : Ver 1
# hub_module = hub.load('./module1') # Ver 1
# hub_module = hub.load('./module2') # Ver 2
# hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/1') # Ver 1
# hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2') # Ver 2

stylized_image = hub_module(tf.constant(content_image), tf.constant(style_image))[0]
result = tensor_to_image(stylized_image)

# Output 경로 설정
result.save(option.output_img)
print("Success")
