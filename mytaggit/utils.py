from pykakasi import kakasi
import re
__all__ = ['Kakasi']


class Kakasi:
    _instance = None

    def __init__(self, **kwargs):
        opts = {
            'H': 'a', 'K': 'a', 'J': 'a',
            'S': '-', 's': True}
        opts.update(kwargs)

        self.kakasi = kakasi()
        for k, v in opts.items():
            self.kakasi.setMode(k, v)
        self.converter = self.kakasi.getConverter()

    def convert(self, text):
        res = self.converter.do(text)
        return re.sub(r'--+', '-', re.sub(r'\s+', '-', res))

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


def to_roman(text):
    return Kakasi().convert(text)