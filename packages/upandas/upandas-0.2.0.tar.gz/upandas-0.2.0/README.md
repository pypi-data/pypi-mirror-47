# upandas

upandas makes it easy to use quantities with uncertainties in pandas DataFrames and Series.

upandas relies on the excellent [uncertainties]() package, and of course [pandas](). 

```python
# A dataframe with nominal values in columns x and y,
# and their respective uncertainties in u_x, u_y

In [1]: n=3; df = pd.DataFrame({ 'x': randn(n),  'u_x': 0.1*rand(n),
   ...:                   'y': randn(n), 'u_y': 0.1*rand(n) })

In [2]: df
Out[2]:
          x       u_x         y       u_y
0 -1.735288  0.014020 -1.426411  0.093879
1 -0.677756  0.084329 -1.254212  0.034601
2  2.410181  0.054435 -1.611307  0.020315

# Convert col/u_col pairs to uarray columns
In [3]: uf = separate_to_u(df)
In [4]: uf
Out[4]:
                x               y
0  -1.735+/-0.014    -1.43+/-0.09
1    -0.68+/-0.08  -1.254+/-0.035
2     2.41+/-0.05  -1.611+/-0.020

# Operate on columns in the DataFrame as usual,
# but propagate the uncertainties
In [5]: uf['xy2'] = uf['x'] * uf['y']**2
In [6]: uf
Out[6]:
                x               y           xy2
0  -1.735+/-0.014    -1.43+/-0.09    -3.5+/-0.5
1    -0.68+/-0.08  -1.254+/-0.035  -1.07+/-0.15
2     2.41+/-0.05  -1.611+/-0.020   6.26+/-0.21

# Convert back to a conventional dataframe
# for e.g. storage to HDF5.
In [17]: u_to_separate(uf)
Out[17]:
          x       u_x         y       u_y       xy2     u_xy2
0 -1.735288  0.014020 -1.426411  0.093879 -3.530698  0.465620
1 -0.677756  0.084329 -1.254212  0.034601 -1.066143  0.145112
2  2.410181  0.054435 -1.611307  0.020315  6.257576  0.211830
```

## Getting Started

### Prerequisites

upandas relies on uncertainties and pandas,
but pip will install these if needed. 

### Installing

```
pip install upandas
```

## Running the tests

Basic tests are included, using [pytest](https://docs.pytest.org/en/latest/index.html). In the base directory:
```
pytest tests 
```
or just `make test`.

## Usage

upandas so far provides only two functions:

- `separate_to_u(df)`: converts col, u_col pairs to a uarray column col.
- `u_to_separate(df)`: converts a uarray column col to a pair col, u_col.

If applied to a Series, these functions look at the 'row' index rather than columns.

## Built With

- [poetry](https://poetry.eustace.io/)

Note that as a 'modern' python project and uses [pyproject.toml](pyproject.toml) rather than setuptools `setup.py`.

If you want to develop locally, pull this repository and execute... TBC.

## Contributing

Please do send me pull requests!

## Versioning

We use [SemVer](http://semver.org/) for versioning. 

## Authors

- *Lincoln Turner* - [lincolndturner](https://bitbucket.org/lincolndturner)

## TODO

- MultiIndex support.
- Make ufloats a pandas [extensions type](https://pandas.pydata.org/pandas-docs/stable/development/extending.html#extension-types), although not clear this is needed.
- Make uarrays a pandas [https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.extensions.ExtensionArray.html#pandas.api.extensions.ExtensionArray] extension array, although again not clear if this is needed.
- Register pandas [custom accessors](https://pandas.pydata.org/pandas-docs/stable/development/extending.html#registering-custom-accessors), so that we can be a bit more pythonic about the conversion: `df.u.from_separate()...`,
- ... and `df.u.nomnal_values`, `df.u.std_devs`.
- More tests

## License

This project is licensed under the Monash/BSD 2-Clause License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Inspired by the extensive support of uncertainties 
in [lyse](https://bitbucket.org/labscript_suite/lyse/),
as part of the [labscript suite](http://labscriptsuite.org/).
