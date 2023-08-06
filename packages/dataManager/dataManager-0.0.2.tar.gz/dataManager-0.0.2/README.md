# DataManager

A simple library to simplify data handling in deep learning environments. With an API non dissimilar to PyTorch DataLoader

## Usage

```python
    from dataManager import Manager as DataManager

    dataFunction = lambda x: (reduceImageSize(inputImages,x), inputLabels[x], ...)
    # Initialize Data Providers
    dataManger = DataManger(
        data = dataFunction,
        bz = 32,  
        stochasticSampling = True,
        indexingShape = [dataInput.shape[0]] 
    )

    # provide the data for the tenth batch
    i = 10
    dataManger(i, stochastic = False).shape
    # > (32, ...)
```

## API

### ```__init__(data, indexingShape = None, bz = 32, stochasticSampling = True)```

* ```data: numpy.array or function```: Data to be used during training. If a numpy array is provided the data will be wrapped in a function. The input function should only take one argument which are the indexes of the elements for the data batch.

* ```indexingShape: array```: Array of size 1 or 2. Used to provide the data at each batch. If the array had dim 1, then a list of indexes will be provided. If ```stochasticSampling``` is set to false then the indexes will be ordered from 0 to  (indexingShape - indexingShape%bz), else if the array is dim 2 the indexes will be provided from left to right and from top to bottom of the 2d matrix, in this case we also only provide as many indexes as is possible to provide with full batches.

* ```stochasticSampling: bool```: if true, the indexes provided are sampled in a totally random way with equal probability for each element. For each batch all indexes will be different, but uniqueness of indexes is not guaranteed though batches.

### ```__call__(i, stochastic = None)```
- ```i: integer```: index of the current batch, starting from 0
- ```stochastic: bool```: if stochasticSampling is to be used or not

## Notes:
StochasticSampling overwrites ordered indexing.

## Undocumented Functions:
StochasticSampling overwrites ordered indexing.
* self.getBatch(self, step, bz): return an ordered batch of indexes at a given step
* self.getBatch(self, step, bz): return an ordered batch of indexes at a given step
* self.getStochasticBatch(self, shape, bz): return a randomly picked set of elements with equal probability. Shape is the specific shape defaults to indexingShape if nothing given.
