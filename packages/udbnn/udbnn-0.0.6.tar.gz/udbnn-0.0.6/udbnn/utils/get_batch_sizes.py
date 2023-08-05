import numpy as np
from extra_keras_utils import set_seed

def get_batch_sizes(resolution:int, minimum:int, size:int, seed:int, base:float=1.1, delta:int=10):
    set_seed(seed)
    batch_sizes = base**np.arange(delta, delta+resolution)
    np.random.shuffle(batch_sizes)
    return minimum+np.ceil(batch_sizes/np.max(batch_sizes)*(size-minimum)).astype(int)