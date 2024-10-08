#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import xarray as xr
from typing import Iterable


class ReadOFormat(xr.Dataset):
    """reads Matrix from a file
    """
    __slots__ = ()
    _target_cols_zones = ['zone_no', 'zone_name']
    _target_cols_matrix = ['origins', 'destinations', 'values']

    def __init__(self,
                 zonefile: str,
                 matrixfile: str,
                 cols_zones: Iterable[str] = None,
                 cols_matrix: Iterable[str] = None
                 ):
        """
        Parameters
        ----------
        zonefile:
            the filepath to the file with zone names
        matrixfile:
            the filepath to the file with the matrix values
        cols_zones:
            the column with the zones
        cols_matrix:
            the columnsto use [column_with_zone_no, column_with_zone_name]
        """
        super().__init__()
        self.read_zones_csv(zonefile, cols_zones)
        self.read_matrix_csv(matrixfile, cols_matrix)

    def read_matrix_csv(self, filename: str, cols_matrix: Iterable[str]):
        """
        Reads a matrix from a csv-file and stores it in self['matrix']

        Parameters
        ----------
        filename:
            the filepath of the input file
        cols_matrix:
            the columns to use
        """
        target_cols = self._target_cols_matrix
        data_cols = cols_matrix
        pkey = target_cols[:2]

        ds = self.read_file_to_ds(data_cols, filename, target_cols, pkey)
        self['matrix'] = ds['values']
        m = self['matrix']
        m.data[np.isnan(m.data)] = 0

    def read_zones_csv(self, filename: str, cols_zones: Iterable[str]):
        """
        Reads a matrix from a csv-file and stores it as coordinates


        Parameters
        ----------
        filename:
            the filepath of the input file
        cols_matrix:
            the columns to use [column_with_zone_no, column_with_zone_name]
        """
        target_cols = self._target_cols_zones
        data_cols = cols_zones
        pkey = target_cols[0]
        col_name = target_cols[1]

        ds = self.read_file_to_ds(data_cols, filename, target_cols, pkey)
        dims = self._target_cols_zones[:1] + self._target_cols_matrix[:2]
        # set as origins and destinations
        for dim in dims:
            renamed_ds = ds.rename({pkey: dim})
            self[dim] = renamed_ds[dim]
            name_dim = f'name_{dim}'
            self.coords[name_dim] = xr.IndexVariable(dims=[dim],
                                                     data=renamed_ds[col_name])

    def read_file_to_ds(self,
                        data_cols: Iterable[str],
                        filename: str,
                        target_cols: Iterable[str],
                        pkey: str) -> xr.Dataset:
        """
        reads a file into a Dataset

        Parameters
        ----------
        data_cols:
            the columns with the data
        filename:
            the full filepyth
        target_cols:
            the target colum names
        pkey:
            the primary key

        Returns
        -------
        :
            the Dataset with the results
        """
        df = pd.read_csv(filename, usecols=data_cols)
        if not data_cols:
            # take the first columns of the table
            data_cols = df.columns.values[:len(target_cols)]

        # rename the columns to the target names
        msg = 'wrong number of columns specified'
        assert len(data_cols) == len(target_cols), msg
        rename_cols = dict(zip(data_cols,
                               target_cols))
        df.rename(columns=rename_cols, inplace=True)

        ds = df.set_index(pkey).sort_index().to_xarray()
        return ds
