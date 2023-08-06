# BxTorch

BxTorch is a high-level library for working with [PyTorch](https://pytorch.org).
It is designed to make PyTorch much simpler in the most common cases. Yet,
it is engineered to be highly extensible in order to preserve PyTorch's
flexibility --- while relieving you from writing boilerplate code.

Have a look at [BxModels](https://gitlab.lrz.de/kdd/bxmodels) if you want to
use implementations of well-known machine learning models.

## Installation

BxTorch is available on PyPi, so simply run the following command:

```bash
pip install bxtorch
```

The package will install the dependencies specified [here](requirements.txt).
If you plan to use plotting features of BxTorch, make sure to also install the
following packages:

```txt
matplotlib
```

## Features

Generally, BxTorch provides an object-oriented approach to abstracting PyTorch's
API. The core design objective is to provide an API both as simple and as
extensible as possible --- usually at the expense of some milliseconds of
execution time. Be aware that the goal of this library is *not* to maximize
performance in cases where it is not needed.

This does not mean that BxTorch does not care about performance: in fact, the
library has built-in support for multi-GPU training, both within a single
process and split over multiple processes.

It must be emphasized that BxTorch is not meant to be a wrapper for PyTorch as
Keras is for TensorFlow, for example. It only provides *extensions* for PyTorch.

## Documentation

Examples of the usage of BxTorch can be found in the [docs folder](docs).
Method documentation is currently only available as [docstrings](bxtorch).

## License

BxTorch is licensed under the [MIT License](LICENSE).

The logo is modified from [thenounproject.com](https://thenounproject.com),
"Torch by iconsmind.com from the Noun Project".
