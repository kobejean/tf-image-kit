import tensorflow as tf
import numpy as np
import datetime
import time
import os
from PIL import Image

# adapted from https://gist.github.com/dave-andersen/265e68a5e879b5540ebc
# and https://github.com/meereeum/k-meanz/

MAX_ITERS = 1000
PERIOD = 1

def kmeans(filepath, k, wx = 1.0, wy = 1.0, outdir = None):
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
        idxs = tf.constant([(j,k) for j in range(m) for k in range(n)], dtype=tf.float32)
        pixel_array = tf.concat([idxs, tf.to_float(tf.reshape(pixels, shape=(m * n, chann)))], 1)
        # weight the values
        weights = (wx/float(max(m,n)), wy/float(max(m,n)), 1.0/255.0, 1.0/255.0, 1.0/255.0)
        weight_mold = tf.cast(tf.tile([weights], [m * n, 1]), tf.float32)
        weighted_pix_array = tf.multiply(weight_mold, pixel_array)

        cluster_assignments = tf.Variable(tf.zeros([m * n], dtype=tf.int64), name="cluster_assignments")
        centroids = tf.Variable(tf.slice(tf.random_shuffle(weighted_pix_array), [0,0], [k,-1]), name="centroids")

        # Replicate to N copies of each centroid and K copies of each
        # point, then subtract and compute the sum of squared distances.
        rep_centroids = tf.reshape(tf.tile(centroids, [m * n, 1]), [m * n, k, 5])
        rep_pix = tf.reshape(tf.tile(weighted_pix_array, [1, k]), [m * n, k, 5])
        sum_squares = tf.reduce_sum(tf.square(rep_pix - rep_centroids), axis=2)

        # Use argmin to select the lowest-distance point
        best_centroids = tf.argmin(sum_squares, 1)
        did_assignments_change = tf.reduce_any(tf.not_equal(best_centroids, cluster_assignments))

        def bucket_mean(data, bucket_ids, num_buckets):
            total = tf.unsorted_segment_sum(data, bucket_ids, num_buckets)
            count = tf.unsorted_segment_sum(tf.ones_like(data), bucket_ids, num_buckets)
            return total / count

        means = bucket_mean(weighted_pix_array, best_centroids, k)

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
            print()
            print("ITERATION:", iters)
            [changed, _] = session.run([did_assignments_change, do_updates])

            if iters % PERIOD == 0:
                now = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
                outpath = os.path.join(outdir, '{}_k{}_wx{}_wy{}_i{}{}'\
                    .format(basename, k, wx, wy, str(iters).zfill(3), ext))
                [centers, assignments] = session.run([centroids, cluster_assignments])
                end = time.time()
                print("CENTROIDS:")
                print(centers)
                print("ASSIGNMENTS:", assignments)
                # reverse weights
                unweight_mold = 1 / tf.cast(tf.tile([weights], [k, 1]), tf.float32)
                unweighted_centers = tf.multiply(centers, unweight_mold)
                # assign rgb values from centroids
                i_centroids = tf.cast(tf.round(unweighted_centers), tf.uint8)
                cluster_gather = tf.gather(i_centroids, assignments)
                # (m,n,R,G,B) becomes just (R,G,B)
                rgb_slice = tf.slice(cluster_gather, [0,2], [-1,-1])
                print("RGB:")
                print(session.run(rgb_slice))
                final_pixel_array = tf.reshape(rgb_slice, [m, n, chann])

                # encode
                image = session.run(encoder(final_pixel_array))
                with open(outpath, 'wb') as f:
                    f.write(image)

if __name__ == '__main__':

    print("RUNNING")
    abspath = os.path.abspath(os.path.dirname(__file__))
    inputpath = os.path.join(abspath, "input")
    outpath = os.path.join(abspath, "output")
    # docspath = os.path.join(abspath, "docs")

    readpath = os.path.join(inputpath, "kurohime_bike_480x270.jpeg")
    # readpath = os.path.join(inputpath, "kurohime_bike_960x540.jpeg")
    # readpath = os.path.join(inputpath, "kurohime_bike_1920x1080.jpeg")
    # readpath = os.path.join(inputpath, "nagano_train_480x360.jpeg")
    # readpath = os.path.join(inputpath, "nagano_train_960x720.jpeg")

    # readpath = os.path.join(inputpath, "flower_646x348.jpeg")
    # readpath = os.path.join(inputpath, "flower_1856x1392.jpeg")


    # kmeans(readpath, 13, 5.0, 5.0, outpath)
    kmeans(readpath, 50, 5.0, 5.0, outpath)

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
