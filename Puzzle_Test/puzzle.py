from dataclasses import dataclass

import cv2
from sympy import divisors
import numpy as np
from random import shuffle
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


class Piece:
    def __init__(self, data, row, column):
        self.data = data
        self.row = row
        self.column = column

        self.info = (PieceEdge(self.data),
                     PieceEdge(np.rot90(self.data, 1)),
                     PieceEdge(np.rot90(self.data, 2)),
                     PieceEdge(np.rot90(self.data, 3)))

    def get_gradient(self, rotationSelf, piece, rotationPiece):
        return np.array(np.rot90(piece.data, rotationPiece)[:, 0]) - np.array(np.rot90(self.data, rotationSelf)[:, len(self.data) - 1])

    def get_dissimilarity_left(self, rotationSelf, piece, rotationPiece):
        mean = self.info[rotationSelf].meanGradientLeft
        inverseCov = np.linalg.inv(self.info[rotationSelf].covarianceMatrixLeft)

        gradient = self.get_gradient(rotationSelf, piece, rotationPiece)

        return max(sum([(np.array(x) - mean) @ inverseCov @ np.atleast_2d(np.array(x) - mean).T for x in gradient]), 0.00001)

    def get_dissimilarity_right(self, rotationSelf, piece, rotationPiece):
        mean = self.info[rotationSelf].meanGradientRight
        inverseCov = np.linalg.inv(self.info[rotationSelf].covarianceMatrixRight)

        gradient = np.dot(-1, np.array(piece.get_gradient(rotationPiece, self, rotationSelf)))

        return max(sum([(np.array(x) - mean) @ inverseCov @ np.transpose(np.array(x) - mean) for x in gradient]), 0.00001)


class Puzzle:
    def __init__(self, file):
        img = cv2.imread(file)

        n, m = len(img), len(img[0])

        self.P = min(filter(lambda x: x > 20, np.intersect1d(divisors(n), divisors(m))))
        self.N, self.M = n // self.P, m // self.P

        #self.pieces = [Piece(img[x * self.P:(x + 1) * self.P, y * self.P:(y + 1) * self.P], x, y) for x in range(self.N) for y in range(self.M)]
        self.pieces = [Piece(np.rot90(img[x * self.P:(x + 1) * self.P, y * self.P:(y + 1) * self.P], np.random.randint(0, 4)), x, y) for x in range(self.N) for y in range(self.M)]
        shuffle(self.pieces)

        for i in range(len(self.pieces)):
            self.pieces[i].row = i // self.M
            self.pieces[i].column = i % self.M

    def solve(self):
        graph = Graph(self)
        self.pieces = [np.rot90(self.pieces[graph.edges[0][0]].data, graph.edges[0][2]), np.rot90(self.pieces[graph.edges[0][1]].data, graph.edges[0][3])]

    def save(self, name='solved.png'):
        img = np.uint8(np.array([[[0, 0, 0]] * self.M * self.P] * self.N * self.P))
        for i in range(self.N):
            for j in range(self.M):
                img[i * self.P:(i + 1) * self.P, j * self.P:(j + 1) * self.P] = self.pieces[i * self.M + j].data

        cv2.imwrite(name, img)

    def show(self, title='photo'):
        self.N = 1
        self.M = 2
        img = np.uint8(np.array([[[0, 0, 0]] * self.M * self.P] * self.N * self.P))
        for i in range(self.N):
            for j in range(self.M):
                img[i * self.P:(i + 1) * self.P, j * self.P:(j + 1) * self.P] = self.pieces[i * self.M + j].data

        cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
