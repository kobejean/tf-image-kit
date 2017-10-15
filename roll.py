import tensorflow as tf
import numpy as np
import datetime
import time
import os


def roll(filepath, outdir = None):
    start = time.time()

    is_jpeg = filepath.lower().endswith("jpg") or filepath.lower().endswith("jpeg")
    is_png = filepath.lower().endswith("png")
    assert is_jpeg or is_png, "Image has to be jpeg or png."

    filepath = os.path.expanduser(filepath)
    basename, ext = os.path.splitext(os.path.basename(filepath))

    outdir = os.path.expanduser(outdir if outdir else "")

    decoder = (tf.image.decode_jpeg if is_jpeg else tf.image.decode_png)
    encoder = (tf.image.encode_jpeg if is_jpeg else tf.image.encode_png)

    with tf.Session() as session:

        with open(filepath, 'rb') as f:
            input_image = f.read()

        pixels = decoder(input_image)
        m, n, chann = tf.shape(pixels).eval()
        # with tf.device('/cpu:0'): # for CPU
        pix_32 = tf.cast(pixels, tf.float32)
        with tf.device('/gpu:0'): # for GPU
            rolled_32 = tf.manip.roll(pix_32, shift=[int(m/2), int(n/2)], axis=[0,1])

        rolled = tf.cast(pixels, tf.uint8)

        init = tf.global_variables_initializer()
        session.run(init)
        image = session.run(encoder(rolled))

        init = tf.global_variables_initializer()

        outpath = os.path.join(outdir, '{}_rolled{}'\
            .format(basename, ext))

        with open(outpath, 'wb') as f:
            f.write(image)


if __name__ == '__main__':

    print("RUNNING")
    abspath = os.path.abspath(os.path.dirname(__file__))
    inputpath = os.path.join(abspath, "input")
    outpath = os.path.join(abspath, "output")
    # docspath = os.path.join(abspath, "docs")

    # readpath = os.path.join(inputpath, "kurohime_bike_480x270.jpeg")
    # readpath = os.path.join(inputpath, "kurohime_bike_960x540.jpeg")
    readpath = os.path.join(inputpath, "kurohime_bike_1920x1080.jpeg")
    # readpath = os.path.join(inputpath, "nagano_train_480x360.jpeg")
    # readpath = os.path.join(inputpath, "nagano_train_960x720.jpeg")

    # readpath = os.path.join(inputpath, "flower_464x348.jpeg")
    # readpath = os.path.join(inputpath, "flower_1856x1392.jpeg")


    # kmeans(readpath, 13, 5.0, 5.0, outpath)
    roll(readpath, outpath)

    # for i in range(10,110,20):
    #     kmeans(readpath, i, 0.0, 0.0, outpath)
    #     kmeans(readpath, i, 0.1, 0.1, outpath)
    #     kmeans(readpath, i, 0.5, 0.5, outpath)
    #     kmeans(readpath, i, 1.0, 1.0, outpath)
    #     kmeans(readpath, i, 0.0, 1.0, outpath)
    #     kmeans(readpath, i, 1.0, 0.0, outpath)

    # for i in range(10,110,20):
    #     kmeans(readpath, i, 0.0, 0.0, outpath)
    #     kmeans(readpath, i, 0.1, 0.1, outpath)
    #     kmeans(readpath, i, 0.5, 0.5, outpath)
    #     kmeans(readpath, i, 1.0, 1.0, outpath)
    #     kmeans(readpath, i, 0.0, 1.0, outpath)
    #     kmeans(readpath, i, 1.0, 0.0, outpath)
