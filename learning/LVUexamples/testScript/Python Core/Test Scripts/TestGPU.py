# coding=utf-8

"""
This python script tests GPU computing using theano. This does not
require the virtual environment.
"""

print("Starting TestGPU.py script.")

from theano import function as function
from theano import config as config
from theano import shared as shared
from theano import tensor as tensor
import numpy as np
import time

vector_length = 10 * 384 * 768  # 10 x #cores x # threads per core
iterations = 1000

rng = np.random.RandomState(22)
x = shared(np.asarray(rng.rand(vector_length), config.floatX))
f = function([], tensor.exp(x))

t0 = time.perf_counter()
print("About to start iterations.")
for i in range(iterations):
    r = f()
t1 = time.perf_counter()
print("Looping %d times took %f seconds" % (iterations, t1 - t0))

# The isinstance test is giving us trouble when run through the
# connector. Runs fine on its own, though not a good test.
if np.any([  # isinstance(x.op, tensor.Elemwise)
             # and
           ('Gpu' not in type(x.op).__name__)
           for x in f.maker.fgraph.toposort()]):
    print('Used the cpu')
else:
    print('Used the gpu')
