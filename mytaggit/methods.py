from .utils import to_roman


class Tag(object):

    @classmethod
    def to_roman(cls, text):
        return to_roman(text)
