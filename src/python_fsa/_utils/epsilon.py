# Is this a good use of Python's module's singleton-like behavior?
# Probably not.

class Epsilon:
    symbol = "\u03B5"

    def __str__(self):
        return type(self).symbol


# Don't touch it !
EPSILON = Epsilon()

del Epsilon
