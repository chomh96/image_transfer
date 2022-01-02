import argparse

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--content_img',
        type=str,
        help='content image path',
        required=True)

    parser.add_argument('--style_img',
        type=str,
        help='style image path',
        required=True)

    parser.add_argument('--resize_width',
        type=int,
        help='If set, resize the content, style and result images to the same width')

    parser.add_argument('--model',
        type=int,
        help='The Version of model '
             '(Default : %(default)s)',
        default='1')

    parser.add_argument('--output_img',
        type=str,
        help='The path of the result file  '
             '(Default : %(default)s)',
        default='./image/result/result.png')

    return parser.parse_args()
