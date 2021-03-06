# tf-image-kit

<!--[alt](media/kmeans_kurohime_bike_1920x1080_k50_wx3.0_wy1.0_i139.jpeg)-->


### k-means

Here we are using k-means clustering to cluster `(x,y,r,g,b)` values. This creates an image segmentation effect.

<p align="center">
    <a href="media/input/nagano_train_960x720.jpeg"><img src="media/input/nagano_train_480x360.jpeg" alt="image"  width="240"/></a>
    <a href="media/input/kurohime_bike_1920x1080.jpeg"><img src="media/input/kurohime_bike_480x270.jpeg" alt="image"  width="240"/></a>
    <a href="media/input/flower_1856x1392.jpeg"><img src="media/input/flower_464x348.jpeg" alt="image"  width="240"/></a>
</p>
<p align="center">
                                    |
</p>
<p align="center">
                                    v
</p>
<p align="center">
    <a href="media/kmeans_nagano_train_480x360_k75_wx3.0_wy3.0_40f.gif"><img src="media/kmeans_nagano_train_480x360_k75_wx3.0_wy3.0_40f.gif" alt="gif"  width="240"/></a>
    <a href="media/kmeans_kurohime_bike_480x270_k50_wx3.0_wy1.0_40f.gif"><img src="media/kmeans_kurohime_bike_480x270_k50_wx3.0_wy1.0_40f.gif" alt="gif"  width="240"/></a>
    <a href="media/kmeans_flower_464x348_k16_wx5.0_wy5.0_40f.gif"><img src="media/kmeans_flower_464x348_k16_wx5.0_wy5.0_40f.gif" alt="gif"  width="240"/></a>
</p>

**Usage:**

```python
from kmeans import *
kmeans(filepath, k, wx = 1.0, wy = 1.0, outdir = None)
```
**Arguments:**
- `filepath` - The file path of the image to apply the k-means effect.
- `k` - The number of means/clusters.
- `wx` - A weight on the x values. Higher values will make it cluster along the x-axis.
- `wy` - A weight on the y values. Higher values will make it cluster along the y-axis.
- `outdir` - The file path to the output directory.



<!-- GIF EXAMPLES

<p align="center">
    <a href="docs/media/kmeans_nagano_train_480x360_k75_wx3.0_wy3.0_40f.gif"><img src="docs/media/kmeans_nagano_train_480x360_k75_wx3.0_wy3.0_40f.gif" alt="gif"  width="480"/></a>
</p>

```python
from kmeans import *
# read from input/nagano_train_480x360.jpeg
kmeans(readpath, 75, 3.0, 3.0, outpath)
```



<p align="center">
    <a href="docs/media/kmeans_kurohime_bike_480x270_k50_wx3.0_wy1.0_40f.gif"><img src="docs/media/kmeans_kurohime_bike_480x270_k50_wx3.0_wy1.0_40f.gif" alt="gif"  width="480"/></a>
</p>

```python
from kmeans import *
# read from input/kurohime_bike_480x270.jpeg
kmeans(readpath, 50, 3.0, 1.0, outpath)
```



<p align="center">
    <a href="docs/media/kmeans_flower_464x348_k16_wx5.0_wy5.0_40f.gif"><img src="docs/media/kmeans_flower_464x348_k16_wx5.0_wy5.0_40f.gif" alt="gif"  width="480"/></a>
</p>

```python
from kmeans import *
# read from input/kmeans_flower_464x348.jpeg
kmeans(readpath, 16, 5.0, 5.0, outpath)
```

-->

---
<a name="example-1"></a>
<p align="center">
    <b>Example 1</b><br/><br/>
    <video width="480" height="360" class="video-js vjs-default-skin" preload="none" poster="media/kmeans_nagano_train_960x720_k5_wx0.5_wy0.5_poster.jpeg" controls data-setup='{"inactivityTimeout": 100, "playbackRates": [0.25, 0.5, 0.75, 1.0] }'>
        <source src="media/kmeans_nagano_train_960x720_k5_wx0.5_wy0.5.mp4" type="video/mp4">
        <!-- link to video if <video> tag fails-->
        <a href="https://drive.google.com/open?id=0By-CMfnYF6bZcmRhczg3M0xtOWs"><img src="media/kmeans_nagano_train_960x720_k5_wx0.5_wy0.5_thumb@2x.jpeg" alt="video"  width="480"/></a>
    </video>
</p>

```python
from kmeans import *
# read from input/nagano_train_960x720.jpeg
kmeans(readpath, 5, 0.5, 0.5, outpath)
```


---
<a name="example-2"></a>
<p align="center">
    <b>Example 2</b><br/><br/>
    <video width="480" height="270" class="video-js vjs-default-skin" preload="none" poster="media/kmeans_kurohime_bike_1920x1080_k50_wx3.0_wy1.0_poster.jpeg" controls data-setup='{"inactivityTimeout": 100, "playbackRates": [0.25, 0.5, 0.75, 1.0] }'>
        <source src="media/kmeans_kurohime_bike_1920x1080_k50_wx3.0_wy1.0.mp4" type="video/mp4">
        <!-- link to video if <video> tag fails-->
        <a href="https://drive.google.com/open?id=0By-CMfnYF6bZNDNMWW8tNGVNNGM"><img src="media/kmeans_kurohime_bike_1920x1080_k50_wx3.0_wy1.0_thumb_scaled@2x.jpeg" alt="video"  width="480"/></a>
    </video>
</p>

```python
from kmeans import *
# read from input/kurohime_bike_1920x1080.jpeg
kmeans(readpath, 50, 3.0, 1.0, outpath)
```


---
<a name="example-3"></a>
<p align="center">
    <b>Example 3</b><br/><br/>
    <video width="464" height="348" class="video-js vjs-default-skin" preload="none" poster="media/kmeans_flower_1856x1392_k16_wx5.0_wy5.0_poster.jpeg" controls data-setup='{"inactivityTimeout": 100, "playbackRates": [0.25, 0.5, 0.75, 1.0] }'>
        <source src="media/kmeans_flower_1856x1392_k16_wx5.0_wy5.0.mp4" type="video/mp4">
        <!-- link to video if <video> tag fails-->
        <a href="https://drive.google.com/open?id=0By-CMfnYF6bZSWQxa1hqM1FlaWc"><img src="media/kmeans_flower_1856x1392_k16_wx5.0_wy5.0_thumb_scaled@2x.jpeg" alt="video"  width="464"/></a>
    </video>
</p>

```python
from kmeans import *
# read from input/flower_1856x1392.jpeg
kmeans(readpath, 16, 5.0, 5.0, outpath)
```

<!--  EXTRAS -->


---
<a name="example-4"></a>
<p align="center">
    <b>Example 4</b><br/><br/>
    <video width="480" height="270" class="video-js vjs-default-skin" preload="none" poster="media/kmeans_kurohime_bike_1920x1080_k50_wx3.0_wy3.0_poster.jpeg" controls data-setup='{"inactivityTimeout": 100, "playbackRates": [0.25, 0.5, 0.75, 1.0] }'>
        <source src="media/kmeans_kurohime_bike_1920x1080_k50_wx3.0_wy3.0.mp4" type="video/mp4">
        <!-- link to video if <video> tag fails-->
        <a href="https://drive.google.com/open?id=0By-CMfnYF6bZSlUxWmJUYWNuNEE"><img src="media/kmeans_kurohime_bike_1920x1080_k50_wx3.0_wy3.0_thumb_scaled@2x.jpeg" alt="video"  width="480"/></a>
    </video>
</p>

```python
from kmeans import *
# read from input/kurohime_bike_1920x1080.jpeg
kmeans(readpath, 50, 3.0, 3.0, outpath)
```


---
<a name="example-5"></a>
<p align="center">
    <b>Example 5</b><br/><br/>
    <video width="480" height="360" class="video-js vjs-default-skin" preload="none" poster="media/kmeans_nagano_train_960x720_k100_wx4.0_wy4.0_poster.jpeg" controls data-setup='{"inactivityTimeout": 100, "playbackRates": [0.25, 0.5, 0.75, 1.0] }'>
        <source src="media/kmeans_nagano_train_960x720_k100_wx4.0_wy4.0.mp4" type="video/mp4">
        <!-- link to video if <video> tag fails-->
        <a href="https://drive.google.com/open?id=0By-CMfnYF6bZM0FCM1VxV0VmdEk"><img src="media/kmeans_nagano_train_960x720_k100_wx4.0_wy4.0_thumb@2x.jpeg" alt="video"  width="360"/></a>
    </video>
</p>

```python
from kmeans import *
# read from input/nagano_train_960x720.jpeg
kmeans(readpath, 100, 4.0, 4.0, outpath)
```


---
<a name="example-6"></a>
<p align="center">
    <b>Example 6</b><br/><br/>
    <video width="480" height="270" class="video-js vjs-default-skin" preload="none" poster="media/kmeans_kurohime_bike_960x540_k100_wx4.0_wy4.0_poster.jpeg" controls data-setup='{"inactivityTimeout": 100, "playbackRates": [0.25, 0.5, 0.75, 1.0] }'>
        <source src="media/kmeans_kurohime_bike_960x540_k100_wx4.0_wy4.0.mp4" type="video/mp4">
        <!-- link to video if <video> tag fails-->
        <a href="https://drive.google.com/open?id=0By-CMfnYF6bZSUQ4MnF1ejNQd0E"><img src="media/kmeans_kurohime_bike_960x540_k100_wx4.0_wy4.0_thumb@2x.jpeg" alt="video"  width="480"/></a>
    </video>
</p>

```python
from kmeans import *
# read from input/kurohime_bike_960x540.jpeg
kmeans(readpath, 100, 4.0, 4.0, outpath)
```
