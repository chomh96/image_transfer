import argparse

def parse_args():
    parser = argparse.ArgumentParser()

# ('--weights', nargs='+', type=float, default=[1.0], choices=[1, 2, 3], help='')

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

    parser.add_argument('--module_path',
        type=str,
        help='The path of the hub_module '
             '(Default : %(default)s)',
        default='./module1')

    parser.add_argument('--output_img',
        type=str,
        help='The path of the result file  '
             '(Default : %(default)s)',
        default='./result.png')

    return parser.parse_args()
