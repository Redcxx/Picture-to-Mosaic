import math
import argparse
from PIL import Image


def get_avg_rgb(image):
    bands = image.getdata()
    r_sum = 0
    g_sum = 0
    b_sum = 0
    for band in bands:
        r_sum += band[0]
        g_sum += band[1]
        b_sum += band[2]
    total = len(bands)
    r_avg = r_sum // total
    g_avg = g_sum // total
    b_avg = b_sum // total

    return (r_avg, g_avg, b_avg)

def get_bottom_point(width, height, length, max_width, max_height):

    bottom_x = width + length
    bottom_y = height + length

    if bottom_x > max_width:
        bottom_x = max_width

    if bottom_y > max_height:
        bottom_y = max_height

    return (bottom_x, bottom_y)



def make(image_path, chunk_size):
    print('Generating images ...')
    source = Image.open(image_path)
    image_width, image_height = source.size

    background = Image.new('RGB', (image_width, image_height), 'black')

    total = math.ceil(image_height / chunk_size) * math.ceil(image_width / chunk_size)
    curr = 0

    for height in range(0, image_height, chunk_size):
        for width in range(0, image_width, chunk_size):

            bottom_x, bottom_y = get_bottom_point(width, height, chunk_size, image_width, image_height)

            curr_area = source.crop((width, height, bottom_x, bottom_y))

            replace_area = Image.new('RGB', (chunk_size, chunk_size), get_avg_rgb(curr_area))

            background.paste(replace_area, (width, height))

            curr += 1
            print('\r >>> {} / {} => {}%'.format(curr, total, math.ceil((curr / total) * 100)), end='')

    print(' done')

    return background

def main():
    parser = argparse.ArgumentParser(description='build image from images')
    parser.add_argument('source', help='the image to stimulate')
    parser.add_argument('dest', help='the output file without extension')
    parser.add_argument('size', help='size of each mosaic', type=int)
    args = parser.parse_args()
    background = make(args.source, args.size)
    print('Saving file ... ', end='')
    output_file = args.dest + '.jpg'
    background.save(output_file)
    print('done => {}'.format(output_file))


if __name__ == '__main__':
    main()
