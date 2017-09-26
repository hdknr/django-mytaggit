# coding: utf-8
from .utils import Kakasi


class Tag(object):

    @classmethod
    def to_roman(cls, text):
        return Kakasi().convert(text)
