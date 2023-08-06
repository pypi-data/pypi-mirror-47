#### **_this repo is under development and not stable!_**

# napari

### multi-dimensional image viewer for python

[![License](https://img.shields.io/pypi/l/napari.svg)](https://github.com/napari/napari/raw/master/LICENSE)
[![Build Status](https://api.cirrus-ci.com/github/Napari/napari.svg)](https://cirrus-ci.com/napari/napari)
[![Python Version](https://img.shields.io/pypi/pyversions/napari.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/napari.svg)](https://pypi.org/project/napari)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/napari.svg)](https://pypistats.org/packages/napari)
[![Development Status](https://img.shields.io/pypi/status/napari.svg)](https://github.com/napari/napari)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

**napari** is a fast, interactive, multi-dimensional image viewer for Python. It's designed for browsing, annotating, and analyzing large multi-dimensional images. It's built on top of `PyQt` (for the GUI), `vispy` (for performant GPU-based rendering), and the scientific Python stack (`numpy`, `scipy`).

We're developing **napari** in the open! But the project is in a **pre-alpha** stage. You can follow progress on this repository, test out new versions as we release them, and contribute ideas and code. Expect **breaking changes** from patch to patch.

## installation

**napari** can be installed on most Mac OS X and Linux systems with Python 3.6 or 3.7 by calling 

```sh
$ pip install napari
```

(We're working on adding Windows support.)

To install from the master branch on Github use

```sh
$ pip install git+https://github.com/napari/napari
```

To clone the repository locally and install in editable mode use

```sh
$ git clone https://github.com/napari/napari.git
$ cd napari
$ pip install -e .
```

Note that many of our examples use `data` from `skimage` but `skimage` is otherwise not a dependnecy, so in order to be able to run all the examples you should call

```sh
$ pip install scikit-image
```

## simple example

From inside an IPython shell or Jupyter notebook you can open up an interactive viewer by calling

```python
%gui qt5
from skimage import data
import napari
viewer = napari.view(data.astronaut(), multichannel=True)
```

![image](resources/screenshot-add-image.png)

To do the same thing inside a script call

```python
from skimage import data
import napari
from napari.util import app_context

with app_context():
    viewer = napari.view(data.astronaut())
```

## features

Check out the scripts in the `examples` folder to see some of the functionality we're developing!

For example, you can add multiple images in different layers and adjust them

```python
from skimage import data
from skimage.color import rgb2gray
import napari
from napari.util import app_context

with app_context():
    # create the viewer with four layers
    viewer = napari.view(astronaut=rgb2gray(data.astronaut()),
                         photographer=data.camera(),
                         coins=data.coins(),
                         moon=data.moon())
    # remove a layer
    viewer.layers.remove('coins')
    # swap layer order
    viewer.layers['astronaut', 'moon'] = viewer.layers['moon', 'astronaut']
```

![image](resources/screenshot-layers.png)

You can add markers on top of an image

```python
import numpy as np
from skimage import data
from skimage.color import rgb2gray
import napari
from napari.util import app_context

with app_context():
    # set up viewer
    viewer = napari.Viewer()
    viewer.add_image(rgb2gray(data.astronaut()))
    # create three xy coordinates
    points = np.array([[100, 100], [200, 200], [333, 111]])
    # specify three sizes
    size = np.array([10, 20, 20])
    # add them to the viewer
    markers = viewer.add_markers(points, size=size)
```

![image](resources/screenshot-add-markers.png)

**napari** supports bidirectional communication between the viewer and the Python kernel, which is especially useful in Jupyter notebooks -- in the example above you can retrieve the locations of the markers, including any additional ones you have drawn, by calling

```python
>>> markers.coords
[[100, 100],
 [200, 200],
 [333, 111]]
```

You can render and quickly browse slices of multi-dimensional arrays

```python

import numpy as np
from skimage import data
import napari
from napari.util import app_context

with app_context():
    # create fake 3d data
    blobs = np.stack([data.binary_blobs(length=128, blob_size_fraction=0.05,
                                        n_dim=3, volume_fraction=f)
                     for f in np.linspace(0.05, 0.5, 10)], axis=-1)
    # add data to the viewer
    viewer = napari.view(blobs.astype(float))
```

![image](resources/screenshot-nD-image.png)

You can draw lines and polygons on an image, including selection and adjustment of shapes and vertices, and control over fill and stroke color. Run `examples/add_shapes.py` to generate and interact with the following example.

![image](resources/screenshot-add-shapes.png)

You can also paint pixel-wise labels, useful for creating masks for segmentation, and fill in closed regions using the paint bucket. Run `examples/labels-0-2d.py` to generate and interact with the following example.

![image](resources/screenshot-add-labels.png)

You can change the theme after creating the viewer by setting the `viewer.theme` property. The viewer currently supports `light` and `dark` themes, with `dark` as the default. Run `examples/set_theme.py` to see an example of changing themes.

![image](resources/screenshot-set-theme.png)

## plans

We're working on several features, including 

- support for 3D volumetric rendering
- support for multiple canvases
- a plugin ecosystem for integrating image processing and machine learning tools

See [this issue](https://github.com/napari/napari/issues/141) for some of the key use cases we're trying to enable, and feel free to add comments or ideas!

## contributing

Contributions are encouraged! Please read [our guide](https://github.com/napari/napari/blob/master/CONTRIBUTING.md) to get started. Given that we're in an early stage, you may want to reach out on [Github Issues](https://github.com/napari/napari/issues) before jumping in.
