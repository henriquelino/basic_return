# basic-return

> Manage function returns with a generic class

[![PyPI version][pypi-image]][pypi-url]
[![Build status][build-image]][build-url]
[![GitHub stars][stars-image]][stars-url]
[![Support Python versions][versions-image]][versions-url]



## Getting started

You can [get `basic-return` from PyPI](https://pypi.org/project/basic-return),
which means it's easily installable with `pip`:

```bash
python -m pip install basic-return
```


## Example usage

```python

from basic_return.BasicReturn import BasicReturn
def function(a, b, c=30, d=50):
    br = BasicReturn()

    if a < 10:
        br.status = 10
        br.message = "param a is less than 10"
        br.payload = {"something": 123456789}
        return br

    if b > 20:
        br.status = -10
        br.message = "param b is bigger than 20"
        return br

    br.status = 20
    br.message = "param a is less than 10"
    return br

br = function(10, 20, d=40)
if br.status < 0:
    print(br.owner_call)  # function(a=10, b=20, c=30, d=40); this is how the function was called so we can replicate the error
    raise Exception(f"Something bad happens: [{br.status}] - {br.message}")


```



## Changelog

Refer to the [CHANGELOG.md](https://github.com/henriquelino/basic_return/blob/main/CHANGELOG.md) file.



<!-- Badges -->

[pypi-image]: https://img.shields.io/pypi/v/basic-return
[pypi-url]: https://pypi.org/project/basic-return/

[build-image]: https://github.com/henriquelino/basic_return/actions/workflows/build.yaml/badge.svg
[build-url]: https://github.com/henriquelino/basic_return/actions/workflows/build.yaml

[stars-image]: https://img.shields.io/github/stars/henriquelino/basic_return
[stars-url]: https://github.com/henriquelino/basic_return

[versions-image]: https://img.shields.io/pypi/pyversions/basic_return
[versions-url]: https://pypi.org/project/basic_return/

