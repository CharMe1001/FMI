import cv2
from sympy import divisors
from numpy import intersect1d, random, array, uint8
from random import shuffle
from scipy.ndimage import rotate


class Piece:
    def __init__(self, data, row, column):
        self.data = data
        self.row = row
        self.column = column


class Puzzle:
    def __init__(self, file):
        img = cv2.imread(file)

        n, m = len(img), len(img[0])

        self.P = min(filter(lambda x: x > 20, intersect1d(divisors(n), divisors(m))))
        self.N, self.M = n // self.P, m // self.P

        self.pieces = [Piece(rotate(img[x * self.P:(x + 1) * self.P, y * self.P:(y + 1) * self.P], angle=90 * random.randint(0, 4)), x, y) for x in range(self.N) for y in range(self.M)]
        shuffle(self.pieces)

        for i in range(len(self.pieces)):
            self.pieces[i].row = i // self.M
            self.pieces[i].column = i % self.M

    def show(self, title='photo'):
        img = uint8(array([[[0, 0, 0]] * self.M * self.P] * self.N * self.P))
        for i in range(self.N):
            for j in range(self.M):
                img[i * self.P:(i + 1) * self.P, j * self.P:(j + 1) * self.P] = self.pieces[i * self.M + j].data

        cv2.imshow('title', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
