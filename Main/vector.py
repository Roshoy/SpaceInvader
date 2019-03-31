import math


class Vector:

    def __init__(self, *args):
        self.v = []
        for a in args:
            self.v.append(a)

    def __len__(self):
        return len(self.v)

    def __contains__(self, x):
        return x in self.v

    def __iter__(self):
        for x in self.v:
            yield x

    def __getitem__(self, item):
        return self.v[item]

    def __setitem__(self, key, value):
        self.v[key] = value

    def magnitude(self):
        return math.sqrt(sum([v**2 for v in self.v]))

    def __truediv__(self, other):
        nv = Vector()
        nv.v = [x/other for x in self.v]
        return nv

    def __mul__(self, other):
        nv = Vector()
        nv.v = [x*other for x in self.v]
        return nv

    def normalized(self):
        return self/self.magnitude()

    def __add__(self, other):
        nv = Vector()
        nv.v = [self[i] + other[i] for i in range(len(self.v))]
        return nv

    def __radd__(self, other):
        nv = Vector()
        nv.v = [self[i] + other[i] for i in range(len(self.v))]
        return nv

    def __sub__(self, other):
        nv = Vector()
        if len(other) != len(self):
            print("Wyjątek! Zly wymiar wektora")
            return Vector()
        nv.v = [self[i] - other[i] for i in range(len(self))]
        return nv

    def __rsub__(self, other):
        nv = Vector()
        if len(other) != len(self):
            print("Wyjątek! Zly wymiar wektora")
            return Vector()
        nv.v = [other[i] - self[i] for i in range(len(self))]
        return nv

    def __str__(self):
        return str(self.v)
