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

    def afisState(self, f):
        f.write('(Stanga' + ':<barca>' if self.informatie[2] == 1 else '' + ') ' + self.informatie[1] + ' canibali ' + self.informatie[0] + ' misionari ....... (Dreapta' + ':<barca>' if self.informatie[2] == 0 else ') '  + Graf.nrPers - self.informatie[1] + ' canibali ' + Graf.nrPers - self.informatie[0] + ' misionari')

    def afisSolFisier(self, f):
        if self is None:
            return

        self.afisState(f)


class Graf:
    nrPers, nrLocuri = 0, 0

    def __init__(self, nrPers, nrLocuri, start):
        nrPers = nrPers
        nrLocuri = nrLocuri
        self.start = start

        self.g = open('data.out', 'a')

    def scop(self, informatieNod):
        return informatieNod[0] == informatieNod[1] == informatieNod[2] == 0

    def succesori(self, nod):
        sol = []
        info = nod.informatie

        totalM = info[0] if info[2] == 1 else self.nrPers - info[0]
        totalC = info[1] if info[2] == 1 else self.nrPers - info[1]

        for i in range(0, min(Graf.nrLocuri, totalM) + 1):
            for j in range(0, min(Graf.nrLocuri - i, totalC) + 1):
                informatie = (totalM - i if info[2] == 1 else Graf.nrPers - totalM + i, totalC - j if info[2] == 1 else Graf.nrPers - totalC + j, 1 - info[2]);

                if i + j == 0 or totalM - i < totalC - j or nod.vizitat(informatie):
                    continue

                sol.append(Nod(informatie, nod))

        return sol


def BreadthFirst(graf, NSOL):
    pos = 0
    queue = [Nod(graf.start)]

    for i in range(0, NSOL):
        while pos < len(queue):
            nod = queue[pos]
            pos += 1

            if graf.scop(nod.informatie):
                nod.afisSolFisier(self.g)
                break


            queue += graf.succesori(nod)


def DepthFirst(graf, NSOL, nod=None):
    if nod is None:
        nod = Nod(graf.start)

    if graf.scop(nod.informatie):
        print(nod.informatie)
        NSOL -= 1
        return NSOL

    succ = graf.succesori(nod)

    for nxt in succ:
        NSOL = DepthFirst(graf, NSOL, nxt)

        if NSOL == 0:
            return 0

    return NSOL


if __name__ == '__main__':
    f = open('data.in')

    N, M, NSOL = [int(x) for x in f.read().split()]

    graf = Graf(N, M, (N, N, 1))

    DepthFirst(graf, NSOL)
