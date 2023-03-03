from dataclasses import dataclass

import cv2
from sympy import divisors
import numpy as np
from random import shuffle
from scipy.ndimage import rotate
from graph import Graph


@dataclass
class PieceEdge:
    def __init__(self, data):
        gradientRight = np.array(data[:, 1]) - np.array(data[:, 0])
        self.meanGradientRight = np.array([np.mean(gradientRight[:, 0]), np.mean(gradientRight[:, 1]), np.mean(gradientRight[:, 2])])
        self.covarianceMatrixRight = np.cov(np.transpose(np.concatenate((gradientRight, np.array([[0, 0, 0], [1, 1, 1], [-1, -1, -1], [0, 0, 1], [0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]])))))

        p = len(data)
        gradientLeft = np.array(data[:, p - 1]) - np.array(data[:, p - 2])
        self.meanGradientLeft = np.array([np.mean(gradientLeft[:, 0]), np.mean(gradientLeft[:, 1]), np.mean(gradientLeft[:, 2])])
        self.covarianceMatrixLeft = np.cov(np.transpose(np.concatenate((gradientLeft, np.array([[0, 0, 0], [1, 1, 1], [-1, -1, -1], [0, 0, 1], [0, 1, 0], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]])))))
    gradient: []
    meanGradient: []
    covarianceMatrix: []


class Piece:
    def __init__(self, data, row, column):
        self.data = data
        self.row = row
        self.column = column

        self.info = (PieceEdge(self.data),
                     PieceEdge(rotate(self.data, angle=90)),
                     PieceEdge(rotate(self.data, angle=180)),
                     PieceEdge(rotate(self.data, angle=270)))

    def get_gradient(self, rotationSelf, piece, rotationPiece):
        return np.array(rotate(piece.data, angle=90 * rotationPiece)[:, 0]) - np.array(rotate(self.data, angle=90 * rotationSelf)[:, len(self.data) - 1])

    def get_dissimilarity(self, rotationSelf, piece, rotationPiece):
        mean = self.info[rotationSelf].meanGradientLeft
        if np.array_equal(self.info[rotationSelf].covarianceMatrixLeft, [[0, 0, 0], [0, 0, 0], [0, 0, 0]]):
            return 0.00001
        inverseCov = np.linalg.inv(self.info[rotationSelf].covarianceMatrixLeft)

        return max(sum([np.matmul(np.matmul((np.array(x) - mean), inverseCov), np.transpose(np.array(x) - mean)) for x in self.get_gradient(rotationSelf, piece, rotationPiece)]), 0.00001)


class Puzzle:
    def __init__(self, file):
        img = cv2.imread(file)

        n, m = len(img), len(img[0])

        self.P = min(filter(lambda x: x > 20, np.intersect1d(divisors(n), divisors(m))))
        self.N, self.M = n // self.P, m // self.P

        self.pieces = [Piece(rotate(img[x * self.P:(x + 1) * self.P, y * self.P:(y + 1) * self.P], angle=90 * np.random.randint(0, 4)), x, y) for x in range(self.N) for y in range(self.M)]
        shuffle(self.pieces)

        for i in range(len(self.pieces)):
            self.pieces[i].row = i // self.M
            self.pieces[i].column = i % self.M

    def solve(self):
        graph = Graph(self)

    def show(self, title='photo'):
        img = np.uint8(np.array([[[0, 0, 0]] * self.M * self.P] * self.N * self.P))
        for i in range(self.N):
            for j in range(self.M):
                img[i * self.P:(i + 1) * self.P, j * self.P:(j + 1) * self.P] = self.pieces[i * self.M + j].data

        cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
