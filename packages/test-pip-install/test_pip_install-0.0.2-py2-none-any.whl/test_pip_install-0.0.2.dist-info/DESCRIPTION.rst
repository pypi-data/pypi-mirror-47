# Test if `pip install` is working

_This is a basic package that can be used in order to test if `pip install` is
properly working._


## Description

This package has no external dependencies. It should be compatible down to
`Python 2.7`.

Once installed with `pip`, this package should export the `test-pip-install`
script. The installation can then be tested from a terminal by running:

```
>> test-pip-install
```

or

```
>> python -m test_pip_install
```

If the package has been properly installed, you should see something like:

```
running Python {version} from {path/to/current/python}
```


## License

This package is distributed under the LGPL-3.0 license. See the provided
[`LICENSE`][LICENSE] and [`COPYING.LESSER`][COPYING] files.


[COPYING]: https://github.com/niess/test-pip-install/blob/master/COPYING.LESSER
[LICENSE]: https://github.com/niess/test-pip-install/blob/master/LICENSE


