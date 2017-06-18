import tensorflow as tf
import numpy as np
import datetime
import time
import os
from PIL import Image

# adapted from https://gist.github.com/dave-andersen/265e68a5e879b5540ebc
# and https://github.com/meereeum/k-meanz/

MAX_ITERS = 1000

def kmeans(filepath, k, outdir = None):
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
        # session.run(init)


        with open(filepath, 'rb') as f:
            img_str = f.read()
        pixels = decoder(img_str)
        m, n, chann = tf.shape(pixels).eval()
        idxs = tf.constant([(j,k) for j in range(m) for k in range(n)], dtype=tf.float32)
        pix_array = tf.concat([idxs, tf.to_float(tf.reshape(pixels, shape=(m * n, chann)))], 1)

        cluster_assignments = tf.Variable(tf.zeros([m * n], dtype=tf.int64))
        centroids = tf.Variable(tf.slice(tf.random_shuffle(pix_array), [0,0], [k,-1]), name="centroids")

        # Replicate to N copies of each centroid and K copies of each
        # point, then subtract and compute the sum of squared distances.
        rep_centroids = tf.reshape(tf.tile(centroids, [m * n, 1]), [m * n, k, 5])
        rep_pix = tf.reshape(tf.tile(pix_array, [1, k]), [m * n, k, 5])
        sum_squares = tf.reduce_sum(tf.square(rep_pix - rep_centroids), axis=2)

        # Use argmin to select the lowest-distance point
        best_centroids = tf.argmin(sum_squares, 1)
        did_assignments_change = tf.reduce_any(tf.not_equal(best_centroids, cluster_assignments))

        def bucket_mean(data, bucket_ids, num_buckets):
            total = tf.unsorted_segment_sum(data, bucket_ids, num_buckets)
            count = tf.unsorted_segment_sum(tf.ones_like(data), bucket_ids, num_buckets)
            return total / count

        means = bucket_mean(pix_array, best_centroids, k)

        # Do not write to the assigned clusters variable until after
        # computing whether the assignments have changed - hence with_dependencies
        with tf.control_dependencies([did_assignments_change]):
            do_updates = tf.group(
                centroids.assign(means),
                cluster_assignments.assign(best_centroids))

        init = tf.global_variables_initializer()

        session.run(init)
        changed = True
        iters = 0

        while changed and iters < MAX_ITERS:
            iters += 1
            print("ITERATION:", iters)
            [changed, _] = session.run([did_assignments_change, do_updates])


            if iters % 10 == 0:
                now = datetime.datetime.today().strftime('%Y%m%d_%H%M')
                outpath = os.path.join(outdir, '{}_{}_k{}_{}{}'.format(basename, now, k, iters, ext))
                [centers, assignments] = session.run([centroids, cluster_assignments])
                end = time.time()
                print(("Found in %.2f seconds" % (end-start)), iters, "iterations")
                print("Centroids:")
                print(centers)
                print("Cluster assignments:", assignments)

                print("Period rgbs:")
                i_centroids = tf.cast(tf.round(centers), tf.uint8)
                cluster_gather = tf.gather(i_centroids, assignments)
                rgb_slice = tf.slice(cluster_gather, [0,2], [-1,-1])
                print(session.run(cluster_gather))
                print(session.run(rgb_slice))

                fin_pix = tf.reshape(rgb_slice, [m, n, chann])
                # # print(session.run(tf.shape(pix_array)))
                image = session.run(encoder(fin_pix))

                with open(outpath, 'wb') as f:
                    f.write(image)

        now = datetime.datetime.today().strftime('%Y%m%d_%H%M')
        outpath = os.path.join(outdir, '{}_{}_k{}_{}{}'.format(basename, now, k, iters, ext))

        [centers, assignments] = session.run([centroids, cluster_assignments])
        end = time.time()
        print(("Found in %.2f seconds" % (end-start)), iters, "iterations")
        print("Centroids:")
        print(centers)
        print("Cluster assignments:", assignments)

        print("Final rgbs:")
        i_centroids = tf.cast(tf.round(centers), tf.uint8)
        cluster_gather = tf.gather(i_centroids, assignments)
        rgb_slice = tf.slice(cluster_gather, [0, 2], [-1, -1])
        print(session.run(i_centroids))
        print(session.run(rgb_slice))

        fin_pix = tf.reshape(rgb_slice, [m, n, chann])
        # # print(session.run(tf.shape(pix_array)))
        image = session.run(encoder(fin_pix))

        with open(outpath, 'wb') as f:
            f.write(image)



def _image_to_data(filepath, decoder):
        """Convert image to 1D array of image data: (m, n, R, G, B) per pixel"""
        with open(filepath, 'rb') as f:
            img_str = f.read()
        pixels = decoder(img_str)
        m, n, chann = tf.shape(pixels).eval()
        idxs = tf.constant([(j,k) for j in range(m) for k in range(n)], dtype=tf.float32)
        return tf.concat([idxs, tf.to_float(tf.reshape(pixels, shape=(m * n, chann)))], 1)

# filepath="output/input/img.png"
# print(os.path.expanduser(filepath))
# print(os.path.splitext(os.path.basename(filepath))[0])
print("RUNNING")
abspath = os.path.abspath(os.path.dirname(__file__))
inputpath = os.path.join(abspath, "input")
outpath = os.path.join(abspath, "output")
ntreadpath = os.path.join(inputpath, "nagano_train.jpeg")
kbreadpath = os.path.join(inputpath, "kurohime_bike.jpeg")

# kmeans(ntreadpath, 10, outpath)
# kmeans(ntreadpath, 20, outpath)
# kmeans(ntreadpath, 30, outpath)
# kmeans(ntreadpath, 40, outpath)
# kmeans(ntreadpath, 50, outpath)

kmeans(kbreadpath, 10, outpath)
kmeans(kbreadpath, 20, outpath)
kmeans(kbreadpath, 30, outpath)
kmeans(kbreadpath, 40, outpath)
kmeans(kbreadpath, 50, outpath)
