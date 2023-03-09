from queue import PriorityQueue
from time import time

# informatii despre un nod din arborele de parcurgere (nu nod din graful initial)
class NodParcurgere:
    def __init__(self, info, parinte=None, g=0, h=0):
        self.g = g
        self.f = g + h
        self.info = info  # eticheta nodului, de exemplu: 0,1,2...
        self.parinte = parinte  # parintele din arborele de parcurgere

    def drumRadacina(self):
        l = []
        nod = self
        while nod:
            l.insert(0, nod)
            nod = nod.parinte
        return l


    def vizitat(self): #verifică dacă nodul a fost vizitat (informatia lui e in propriul istoric)
        nodDrum = self.parinte
        while nodDrum:
            if (self.info == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __str__(self):
        return str(self.info)
    def __repr__(self):
        sir = str(self.info) + " " + str(self.f) + "("
        drum = self.drumRadacina()
        sir += ("->").join([str(n.info) for n in drum])
        sir += ")"
        return sir

    def __eq__(self, other):
        return self.f == other.f
    def __le__(self, other):
        return self.f < other.f or (self.f == other.f and self.g >= other.g)
    def __lt__(self, other):
        return self.f < other.f or (self.f == other.f and self.g > other.g)


class Graph:  # graful problemei

    def __init__(self, vecini, start, scopuri, estimari):
        self.vecini = vecini
        self.nrNoduri = len(vecini)
        self.start = start  # informatia nodului de start
        self.scopuri = scopuri  # lista cu informatiile nodurilor scop
        self.estimari = estimari


    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def succesori(self, nodCurent):
        listaSuccesori = []
        for i in range(len(self.vecini[nodCurent.info])):
            nodNou = NodParcurgere(info=(self.vecini[nodCurent.info][i])[0], parinte=nodCurent, g=nodCurent.g + (self.vecini[nodCurent.info][i])[1], h=self.estimeaza_h((self.vecini[nodCurent.info][i])[0]))
            if not nodNou.vizitat():
                    listaSuccesori.append(nodNou)
        return listaSuccesori

    def scop(self, infoNod):
        return infoNod in self.scopuri

    def estimeaza_h(self, nod):
        return self.estimari[nod]


def binS(lst, nod):
    lft, rgt = 0, len(lst) - 1

    while lft <= rgt:
        mid = (lft + rgt) // 2
        if lst[mid] < nod:
            lft = mid + 1
        else:
            rgt = mid - 1

    return rgt


def aStarSolMultipleList(graf, NSOL):
    start = time()

    lst = []
    lst.append(NodParcurgere(graf.start))

    while len(lst) > 0:
        nodCurent = lst[0]
        lst = lst[1:]

        if graf.scop(nodCurent.info):
            print(repr(nodCurent))
            NSOL -= 1
            if NSOL == 0:
                break

        for next in graf.succesori(nodCurent):
            pos = binS(lst, next)
            lst.insert(pos + 1, next)

    print(time() - start)


def aStarSolMultiple(graf, NSOL):
    start = time()
    pq = PriorityQueue()
    pq.put(NodParcurgere(graf.start))

    while not pq.empty():
        nodCurent = pq.get()
        if graf.scop(nodCurent.info):
            print(repr(nodCurent))
            NSOL -= 1
            if NSOL == 0:
                break

        for next in graf.succesori(nodCurent):
            pq.put(next)
    print(time() - start)


def aStar(graf):
    open = []
    closed = []
    open.append(NodParcurgere(graf.start))

    while len(open) > 0:
        nodCurent = open[0]
        open = open[1:]
        closed.append(nodCurent)

        if graf.scop(nodCurent.info):
            print(repr(nodCurent))
            return

        for next in graf.succesori(nodCurent):
            for i in range(len(closed)):
                if closed[i].info == next.info:
                    del closed[i]
                    break

            found = False
            deleted = False

            for i in range(len(open)):
                if open[i].info == next.info:
                    found = True
                    if next < open[i]:
                        deleted = True
                        del open[i]
                    break

            if found and not deleted:
                continue

            pos = binS(open, next)
            if pos + 1 != len(open) and next.info == open[pos + 1].info:
                del open[pos]

            open.insert(pos + 1, next)


muchii = [
    [(1, 3), (2, 5), (3, 10), (6, 100)],
    [(3, 4)],
    [(3, 4), (4, 9), (5, 3)],
    [(1, 3), (4, 2)],
    [],
    [(4, 4), (6, 5)],
    [(2, 3)]
]

euristica = [0, 1, 3, 1, 0, 4, 0]
#euristica = [0, 1, 6, 1000, 0, 3, 0]


if __name__ == '__main__':
    graf = Graph(muchii, 0, [4, 6], euristica)

    print("A Star Multiple Lista:")
    aStarSolMultipleList(graf, 3)

    print("A Star Multiple Coada Prioritati:")
    aStarSolMultiple(graf, 3)

    print("A Start:")
    aStar(graf)
