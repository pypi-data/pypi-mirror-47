# SimpleDataTransport

Simple python 3 library for transporting data to a remote machine, applying transformations and returning a response.
Formerly [SimpleImageTransport](https://pypi.org/project/SimpleImageTransport/).
## Usage

Start a server on the remote machine:

```python
from SimpleDataTransport import DataReceiver

# Callback takes a single dict with an image and returns a dict of useful data
def example_callback(data):
    img = data["image"]
    return {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}


# Initialize the Flask application
flask_receiver = DataReceiver()
flask_receiver.set_callback(example_callback)
flask_receiver.run()
```

On the local machine you can send an image and get an appropriate response:

```python
from SimpleDataTransport import DataSender
import numpy as np

img = np.zeros((1080, 1920))

response = DataSender(img)
print(response)  # {'message': 'image received. size=1920x1080'}
```