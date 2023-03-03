class Graph:
    def __init__(self, puzzle):
        self.N = len(puzzle.pieces)
        self.edges = []

        for piece_i in range(self.N):
            for piece_j in range(self.N):
                if piece_i == piece_j:
                    continue

                for ki in range(4):
                    for kj in range(4):
                        cost = puzzle.pieces[piece_i].get_dissimilarity(ki, puzzle.pieces[piece_j], kj) + puzzle.pieces[piece_j].get_dissimilarity(kj, puzzle.pieces[piece_i], ki)
                        self.edges.append((piece_i, piece_j, ki, kj, cost))

