class Graph:
    def __init__(self, puzzle):
        self.N = len(puzzle.pieces)
        self.edges = []

        for piece_i in range(self.N):
            for piece_j in range(piece_i + 1, self.N):
                print("Processing (" + str(piece_i) + ", " + str(piece_j) + ")...")
                scores = []

                for ki in range(4):
                    for kj in range(4):
                        cost = puzzle.pieces[piece_i].get_dissimilarity_left(ki, puzzle.pieces[piece_j], kj) + puzzle.pieces[piece_j].get_dissimilarity_right(kj, puzzle.pieces[piece_i], ki)
                        scores.append((piece_i, piece_j, ki, kj, cost))

                scores.sort(key=lambda x: x[4])
                ss = scores[1][4]
                scores = list(map(lambda x: (x[0], x[1], x[2], x[3], x[4] / ss), scores))
                self.edges.extend(scores)

        self.edges.sort(key=lambda x: x[4])
