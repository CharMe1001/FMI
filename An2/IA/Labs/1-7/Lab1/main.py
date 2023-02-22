# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Nod:
    def __init__(self, informatie, parinte=None):
        self.parinte = parinte
        self.informatie = informatie

    def drumRadacina(self):
        if self.parinte is None:
            return [self]
        else:
            return self.parinte.drumRadacina() + [self]

    def vizitat(self, nod):
        if self.informatie == nod:
            return True
        else:
            if self.parinte is None:
                return False
            else:
                return self.parinte.vizitat(nod)

    def __repr__(self):
        if self is None:
            return ""
        else:
            drum = self.drumRadacina()
            return str(self.informatie) + " (" + str(drum[0].informatie) + ''.join(["->" + str(nod.informatie) for nod in drum[1:]]) + ")"

    def __str__(self):
        if self is None:
            return ""
        else:
            return self.informatie


class Graf:
    def __init__(self, vecini, start, scop):
        self.vecini = vecini
        self.start = start
        self.scop = scop

    def scop(self, informatieNod):
        for nod in self.scop:
            if nod == informatieNod:
                return True

        return False

    def succesori(self, nod):
        sol = []

        for nxt in self.vecini[nod.informatie]:
            if not nod.vizitat(nxt):
                sol.append(Nod(nxt, nod))

        return sol


def Breadthfirst(graf):
    nsol = int(input())

    pos = 0
    queue = [Nod(graf[0])]

    for i in range(0, nsol):
        while True:
            nod = queue[pos]
            if graf.scop(nod):
                print(nod.informatie)
                break

            pos += 1

            queue += graf.succesori(nod)


def DepthFirstRec(graf, nod=None, nsol=int(input())):
    if nod is None:
        nod = Nod(graf.start)

    if graf.scop(nod.informatie):
        nsol -= 1
        if nsol == 0:
            return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    l = [[0 for _ in range(2)] for _ in range(2)];
    l[0][0] = 10
    print(l)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
