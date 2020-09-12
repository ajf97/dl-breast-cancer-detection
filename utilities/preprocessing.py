# -*- coding: utf-8 -*-
__author__ = "Alejandro Jerónimo Fuentes"
__date__ = "17/08/2020"

from sklearn.feature_extraction.image import extract_patches_2d
import cv2


class MeanRGBPreprocessor:

    def __init__(self, rgb_values):
        self.rgb_values = rgb_values

    def preprocess(self, image):

        # Dividir la imagen en canales RGB
        (B, G, R) = cv2.split(image.astype("float32"))

        # Restamos los valores de la media a la imagen
        B -= self.rgb_values["B"]
        G -= self.rgb_values["G"]
        R -= self.rgb_values["R"]

        image_merged = cv2.merge([B, G, R])

        return cv2.cvtColor(image_merged, cv2.COLOR_BGR2RGB)


class RandomCropPreprocessor:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def preprocess(self, image):
        return extract_patches_2d(image, (self.height, self.width),
                                  patch_size=1)[0]


class MeanZeroOnePreprocessor:
    @staticmethod
    def preprocess(image):
        return image / 255.0


class ResizePreprocessor:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def preprocess(self, image):
        return cv2.resize(image, (self.height, self.width))