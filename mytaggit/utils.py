# coding: utf-8
from pykakasi import kakasi
__all__ = ['Kakasi']


class Kakasi:
    _instance = None

    def __init__(self):
        self.kakasi = kakasi()
        self.kakasi.setMode('H', 'a')
        self.kakasi.setMode('K', 'a')
        self.kakasi.setMode('J', 'a')
        self.converter = self.kakasi.getConverter()

    def convert(self, text):
        return self.converter.do(text)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance
