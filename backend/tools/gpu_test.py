import tensorflow as tf
from tensorflow.python.client import device_lib

print("TF Version:", tf.__version__)
print("Available Devices:")
print(device_lib.list_local_devices())
