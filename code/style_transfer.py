from module import parser as Parser
import sys
import tensorflow_hub as hub
import PIL.Image
import numpy as np
import tensorflow as tf
import os

# 결과 로그 상태 숨기기
# 0 = all messages are logged (default behavior)
# 1 = INFO messages are not printed
# 2 = INFO and WARNING messages are not printed
# 3 = INFO, WARNING, and ERROR messages are not printed
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


# parser
option = Parser.parse_args()


# 이미지 변환 함수
def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]

    return PIL.Image.fromarray(tensor)


# 이미지 불러오기 함수
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


# Main
if __name__ == '__main__':

    # 컨텐츠(사용자) 이미지 경로 설정
    try:
        content_image = load_img(option.content_img)
    except Exception as e:
        print('Check content_image path')
        sys.exit(0)

    # 스타일 이미지 경로 설정
    try:
        style_image = load_img(option.style_img)
    except Exception as e:
        print('Check style_image path')
        sys.exit(0)

    # 이미지 가로 사이즈 변경
    if option.resize_width:
        content_image = tf.image.resize(
            content_image, (option.resize_width, option.resize_width))
        style_image = tf.image.resize(
            style_image, (option.resize_width, option.resize_width))

    # 모델 선택 [Default: model_v1]
    if option.model:
        if option.model == 1:
            hub_module = hub.load('./tf_model/model_v1')  # Local Model ver 1
            # hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/1')  # Server Model ver 1
        elif option.model == 2:
            hub_module = hub.load('./tf_model/model_v2')  # Local Model ver 2
            # hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')  # Server Model ver 2
        else:
            print('Please input model version to 1 or 2')
            sys.exit(0)

    # Default
    else:
        hub_module = hub.load('./tf_model/model_v1')  # Local Model ver 1
        # hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/1')  # Server Model ver 1

    # 이미지 변환하기
    stylized_image = hub_module(tf.constant(
        content_image), tf.constant(style_image))[0]
    result = tensor_to_image(stylized_image)

    # Output 경로 설정
    result.save(option.output_img)

    print("Success")
    print("Image saved in " + option.output_img)
