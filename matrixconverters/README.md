
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Build Status Linux](https://github.com/MaxBo/matrixconverters/actions/workflows/linux-conda.yml/badge.svg)](https://github.com/MaxBo/matrixconverters/actions/workflows/linux-conda.yml)
[![Build Status Windows](https://github.com/MaxBo/matrixconverters/actions/workflows/windows-conda.yml/badge.svg)](https://github.com/MaxBo/matrixconverters/actions/workflows/windows-conda.yml)
[![codecov](https://codecov.io/gh/MaxBo/matrixconverters/branch/master/graph/badge.svg)](https://codecov.io/gh/MaxBo/matrixconverters)


##matrixconverters:
[![PyPI version](https://badge.fury.io/py/matrixconverters.svg)](https://badge.fury.io/py/matrixconverters)
[![Anaconda-Server Badge](https://anaconda.org/maxbo/matrixconverters/badges/version.svg)](https://anaconda.org/maxbo/matrixconverters)

tools to read and write matrices in the format or PTV VISUM

It implements:

**Reading and writing PTV-Matrices**

It can read and write the following formats:
* Text-Formats: O-Format, V-Format, S-Format
* Binary formats: BI-Format, BK-Format, BL-Format

```
# read a matrix into a xarray-Dataset
from matrixconverters import ReadPTVMatrix, SavePTVMatrix
ds = ReadPTVMatrix(filepath)

# save a xr.Dataset as PTV-Matrix
import xarray as xr
da = xr.DataArray(np.arange(9).reshape(3, 3))
zones = xr.DataArray([100, 200, 300])
names = xr.DataArray(['A-Town', 'B-Village', 'C-City'])
ds = xr.Dataset({'matrix': da,
                 'zone_no': zones,
                 'zone_name': names,})
from matrixconverters.save_ptv import SavePTV
s = SavePTV(ds)
s.savePTVMatrix(file_name=matrix_fn_out, file_type='BK')
```

**Writing PSV-Matrices**
* Programmsystem Verkehr by Software-Kontor Helmert-Hilke)
* File-Types CC and CN

```
from matrixconverters.save_ptv import SavePTV
s = SavePTV(ds)
s.savePSVMatrix(file_name=matrix_fn_out, ftype='CC')
```

**Export xarray-Dataset as compressed NetCDF-File**

```
from matrixconverters.xarray2netcdf import xarray2netcdf
xarray2netcdf(ds, file_path)

ds_saved = xr.open_dataset(file_path)
```

[Documentation](https://maxbo.github.io/matrixconverters/)

# Installation
You can use pip to install the packages (and the requirements like numpy).

```
pip install matrixconverters
```

Another way to handle dependencies is to use [conda](https://conda.io/miniconda.html).

There conda packages for python 3.8-3.12 for windows and linux are generated
in the channel *MaxBo* in [Anaconda Cloud](https://anaconda.org/MaxBo).

```
conda create -n myenv python=3.12
conda activate myenv

conda config --add channels conda-forge
conda config --add channels MaxBo

conda install matrixconverters
```
