# EasyVVUQ

[![Build Status](https://travis-ci.org/UCL-CCS/EasyVVUQ.svg?branch=master)](https://travis-ci.org/UCL-CCS/EasyVVUQ)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/UCL-CCS/EasyVVUQ.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/UCL-CCS/EasyVVUQ/context:python)
[![Documentation Status](https://readthedocs.org/projects/easyvvuq/badge/?version=latest)](https://easyvvuq.readthedocs.io/)

The aim of this library is to facilitate verification, validation and 
uncertainty quantification (VVUQ) for a wide variety of simulations.

Development was funded by the EU Horizon 2020 project [VECMA](http://www.vecma.eu/).

## Requirements

To use the library you will need Python 3.6+.

## Installation using pip

The following should fully install the library:
```
pip3 install easyvvuq
```

## Manual installation from repository

Alternatively, you can manually install EasyVVUQ. First clone the repository to your computer:

```
git clone https://github.com/UCL-CCS/EasyVVUQ.git
```

We are trying to keep dependencies at a minimum but a few are inevitable, to install them use:

```
cd EasyVVUQ/

pip3 install -r requirements.txt
```

Then the library can be installed using:
```buildoutcfg
python3 setup.py install
```

To complete the tests you need to compile (requires `g++`) the `cannonsim` code:
```
make -C tests/cannonsim/src/ 
```

## Getting Started

Documentation, including a basic tutorial, is avalable [here](https://easyvvuq.readthedocs.io).
