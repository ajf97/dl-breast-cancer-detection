# -*- coding: utf-8 -*-
__author__ = "Alejandro Jerónimo Fuentes"
__license__ = "GPL"
__date__ = "August 2020"
__status__ = "Development"

# %% Import packages

import h5py
import os
import numpy as np

# %% Main class


class HDF5Dataset:
    def __init__(self, dims, output, datakey="images", bufSize=1000):

        if os.path.exists(output):
            raise ValueError("La ruta de salida ya existe", output)

        self.db = h5py.File(output, "w")
        self.data = self.db.create_dataset(datakey, dims, dtype="float")
        self.labels = self.db.create_dataset("labels", (dims[0], ),
                                             dtype="int")

        self.bufSize = bufSize
        self.buffer = {"data": [], "labels": []}
        self.idx = 0

    def add(self, rows, labels):
        self.buffer["data"].extend(rows)
        self.buffer["labels"].extend(labels)

        if len(self.buffer["data"]) >= self.bufSize:
            self.flush()

    def flush(self):
        i = self.idx + len(self.buffer["data"])
        self.data[self.idx:i] = np.vstack(self.buffer["data"])
        self.labels[self.idx:i] = np.array(self.buffer["labels"])
        self.idx = i
        self.buffer = {"data": [], "labels": []}

    def storeClassLabels(self, classLabels):
        dt = h5py.special_dtype(vlen=str)
        labelSet = self.db.create_dataset("label_names",
                                          (len(classLabels),), dtype=dt)
        labelSet[:] = classLabels

    def close(self):
        if len(self.buffer["data"]) > 0:
            self.flush()

        self.db.close()