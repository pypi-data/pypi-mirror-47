# sinfo

`sinfo` prints version information for loaded modules in the current session,
Python, the OS, and the CPU. It is designed as a minimum measure to increase
reproducibility and provides similar information as `sessionInfo` in R. The
name is shortened to encourage regular usage through reduced typing =)

## Motivation

`sinfo` is particularly useful when conducting exploratory data analysis in
Jupyter Notebooks. Listing the version numbers of all loaded modules after
importing them is a simple way to ensure a minimum level of reproducibility
while requiring little additional effort. This practice is useful both when
revisiting notebooks and when sharing them with colleagues. `sinfo` is meant to
complement more robust practices such as frozen virtual environments,
containers, and binder Notebooks.

## Installation

`sinfo` can be installed via `pip install sinfo`. It does not rely on a package
manager to find version numbers since it fetches them from the module's version
string. Its only dependency is `stdlib_list`, which is used to distinguish
between standard library and third party modules.

## Usage

```python
import math

import natsort
import numpy
import pandas
from sinfo import sinfo


sinfo()
```


Output:

```
natsort         5.3.3
numpy           1.15.2
pandas          0.23.4
-----
Python 3.6.8 |Anaconda custom (64-bit)| (default, Dec 30 2018, 01:22:34) [GCC 7.3.0]
Linux-4.20.1-arch1-1-ARCH-x86_64-with-arch
-----
Session information updated at 2019-02-03 02:31
```

The default behavior is to only print modules not in the standard library,
which is why the `math` module is omitted above (it can be included by
specifying `print_std_lib=True`). To see not only the explicitly imported
modules but also any dependencies they import, specify `print_implicit=True`.
See the docstring for complete parameter info.

## Background

`sinfo` started as minor modifications of `py_session`, and as it grew it
became convenient to create a new package. `sinfo` was built with the help of
information provided in stackoverflow answers and existing similar packages,
including

- https://github.com/fbrundu/py_session
- https://github.com/jrjohansson/version_information
- https://stackoverflow.com/a/4858123/2166823
- https://stackoverflow.com/a/40690954/2166823
