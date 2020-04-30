import string
import time
from random import randint

class Jedinec:

    def __init__(self, sirka, vyska, prekazky, listy, geny=None):
        # inicializuju sa marametre jedinca
        self.geny = []
        self.sirka = sirka
        self.vyska = vyska
        self.prekazky = prekazky
        self.listy = listy
        # ak vynikol jedinec z rodicov, tak nie je nahodny, hned sa aj vypocita fitness
        if geny != None:
            self.geny = geny
            self.vypocitaj_fitness()

    def generuj_nahodne_geny(self):
        # gen je cislo reprezentujuce vstup na obvode
        obvod = 2*self.sirka + 2*self.vyska

        for i in range(self.sirka + self.vyska):
            random = randint(0, obvod-1)
            self.geny.append(random)

        self.fitness = self.vypocitaj_fitness()

    def vytvor_prazdnu_mapu(self):
        mapa = []
        for i in range(self.vyska):
            mapa.append(self.sirka*[0])
        return mapa


    def vytvor_mapu(self):
        mapa = self.vytvor_prazdnu_mapu()
        smer = ''
        index = 0


        for i in range(len(self.prekazky)):
            mapa[self.prekazky[i][1]][self.prekazky[i][0]] = -1

        for i in range(len(self.listy['z'])):
            mapa[self.listy['z'][i][1]][self.listy['z'][i][0]] = -2

        for i in range(len(self.listy['o'])):
            mapa[self.listy['o'][i][1]][self.listy['o'][i][0]] = -3

        for i in range(len(self.listy['c'])):
            mapa[self.listy['c'][i][1]][self.listy['c'][i][0]] = -4

        # Neboli prejdene ziadne -> 0;
        # boli prejdene zlte -> 1;
        # boli prejdene oranzove -> 2
        # boli prejdene vsetky -> 3

        stav_najdenych_listov = 0
        self.najdene_zlte = 0
        self.najdene_oranzove = 0
        self.najdene_cervene = 0

        for gen in self.geny:
            index += 1

            # Podla hodnoty genu vchadza do mapy, pricom moze vojst zo vsetkych styroch stran
            if gen < self.sirka:
                smer = 'd' #dole
                z_x = gen
                z_y = 0
            elif gen >= self.sirka and gen < self.sirka + self.vyska:
                smer = 'l' #vlavo
                z_x = self.sirka-1
                z_y = gen - self.sirka
            elif gen >= self.sirka + self.vyska and gen < self.sirka * 2 + self.vyska:
                smer = 'h' #hore
                z_x = gen - self.sirka - self.vyska
                z_y = self.vyska-1
            else:
                smer = 'p' #vpravo
                z_x = 0
                z_y = gen - self.sirka * 2 - self.vyska

            # Pokial nevyjde von alebo sa nezasekne, hlada cestu
            while True:
                if mapa[z_y][z_x] == 0 or mapa[z_y][z_x] == -2 or \
                        (mapa[z_y][z_x] == -3 and stav_najdenych_listov == 1) or \
                        (mapa[z_y][z_x] == -4 and stav_najdenych_listov == 2):

                    if mapa[z_y][z_x] == -2:
                        self.najdene_zlte += 1
                        if self.najdene_zlte == len(self.listy['z']):
                            stav_najdenych_listov = 1
                    elif mapa[z_y][z_x] == -3:
                        self.najdene_oranzove += 1
                        if self.najdene_oranzove == len(self.listy['o']):
                            stav_najdenych_listov = 2
                    elif mapa[z_y][z_x] == -4:
                        self.najdene_cervene += 1
                        if self.najdene_cervene == len(self.listy['c']):
                            stav_najdenych_listov = 3

                    mapa[z_y][z_x] = index

                    if smer == 'd':
                        if z_y + 1 < self.vyska and (mapa[z_y+1][z_x] == 0 or \
                                mapa[z_y+1][z_x] == -2 or (mapa[z_y+1][z_x] == -3 and stav_najdenych_listov==1) or \
                                (mapa[z_y+1][z_x] == -4 and stav_najdenych_listov==2)):
                            z_y += 1
                        elif z_y + 1 < self.vyska:
                            if z_x + 1 < self.sirka and (mapa[z_y][z_x+1] == 0 or \
                                mapa[z_y][z_x+1] == -2 or (mapa[z_y][z_x+1] == -3 and stav_najdenych_listov==1) or \
                                (mapa[z_y][z_x+1] == -4 and stav_najdenych_listov==2)):
                                smer = 'p'
                                z_x += 1
                            elif z_x - 1 >= 0 and (mapa[z_y][z_x-1] == 0 or \
                                mapa[z_y][z_x-1] == -2 or (mapa[z_y][z_x-1] == -3 and stav_najdenych_listov==1) or \
                                (mapa[z_y][z_x-1] == -4 and stav_najdenych_listov==2)):
                                smer = 'l'
                                z_x -= 1
                            else:
                                # Zasekne sa
                                return mapa

                    elif smer == 'p':
                            if z_x + 1 < self.sirka and (mapa[z_y][z_x+1] == 0 or \
                                mapa[z_y][z_x+1] == -2 or (mapa[z_y][z_x+1] == -3 and stav_najdenych_listov==1) or \
                                (mapa[z_y][z_x+1] == -4 and stav_najdenych_listov==2)):
                                z_x += 1
                            elif z_x + 1 < self.sirka:
                                if z_y + 1 < self.vyska and (mapa[z_y+1][z_x] == 0 or \
                                mapa[z_y+1][z_x] == -2 or (mapa[z_y+1][z_x] == -3 and stav_najdenych_listov==1) or \
                                (mapa[z_y+1][z_x] == -4 and stav_najdenych_listov==2)):
                                    smer = 'd'
                                    z_y += 1
                                elif z_y - 1 >= 0 and (mapa[z_y-1][z_x] == 0 or \
                                mapa[z_y-1][z_x] == -2 or (mapa[z_y-1][z_x] == -3 and stav_najdenych_listov==1) or \
                                (mapa[z_y-1][z_x] == -4 and stav_najdenych_listov==2)):
                                    smer = 'h'
                                    z_y -= 1
                                else:
                                    # Zasekne sa
                                    return mapa

                    elif smer == 'h':
                            if z_y - 1 >= 0 and (mapa[z_y-1][z_x] == 0 or \
                                mapa[z_y-1][z_x] == -2 or (mapa[z_y-1][z_x] == -3 and stav_najdenych_listov==1) or \
                                (mapa[z_y-1][z_x] == -4 and stav_najdenych_listov==2)):
                                z_y -= 1
                            elif z_y - 1 >= 0:
                                if z_x + 1 < self.sirka and (mapa[z_y][z_x+1] == 0 or \
                                mapa[z_y][z_x+1] == -2 or (mapa[z_y][z_x+1] == -3 and stav_najdenych_listov==1) or \
                                (mapa[z_y][z_x+1] == -4 and stav_najdenych_listov==2)):
                                    smer = 'p'
                                    z_x += 1
                                elif z_x - 1 >= 0 and (mapa[z_y][z_x-1] == 0 or \
                                mapa[z_y][z_x-1] == -2 or (mapa[z_y][z_x-1] == -3 and stav_najdenych_listov==1) or \
                                (mapa[z_y][z_x-1] == -4 and stav_najdenych_listov==2)):
                                    smer = 'l'
                                    z_x -= 1
                                else:
                                    # Zasekne sa
                                    return mapa
                    elif smer == 'l':
                            if z_x - 1 >= 0 and (mapa[z_y][z_x-1] == 0 or \
                                mapa[z_y][z_x-1] == -2 or (mapa[z_y][z_x-1] == -3 and stav_najdenych_listov==1) or \
                                (mapa[z_y][z_x-1] == -4 and stav_najdenych_listov==2)):
                                z_x -= 1
                            elif z_x - 1 >= 0:
                                if z_y + 1 < self.vyska and (mapa[z_y+1][z_x] == 0 or \
                                mapa[z_y+1][z_x] == -2 or (mapa[z_y+1][z_x] == -3 and stav_najdenych_listov==1) or \
                                (mapa[z_y+1][z_x] == -4 and stav_najdenych_listov==2)):
                                    smer = 'd'
                                    z_y += 1
                                elif z_y - 1 >= 0 and (mapa[z_y-1][z_x] == 0 or \
                                mapa[z_y-1][z_x] == -2 or (mapa[z_y-1][z_x] == -3 and stav_najdenych_listov==1) or \
                                (mapa[z_y-1][z_x] == -4 and stav_najdenych_listov==2)):
                                    smer = 'h'
                                    z_y -= 1
                                else:
                                    # Zasekne sa
                                    return mapa
                else:
                    break

        return mapa

    def vypocitaj_fitness(self):
        mapa = self.vytvor_mapu()

        fit = 0

        #spocitaju sa prejdene policka
        for i in range(len(mapa)):
            for j in range(len(mapa[i])):
                if mapa[i][j] > 0:
                    fit += 1

        # ak sa nasli listy, pripocitaj fitness
        fit += 20*self.najdene_zlte + 40*self.najdene_oranzove + 60*self.najdene_cervene

        # exponencialne zvysovanie fitness
        self.fitness = pow(fit, 2)
        return fit

    def vypis_mapu(self):
        mapa = self.vytvor_mapu()
        for i in range(len(mapa)):
            for j in range(len(mapa[i])):
                print("{:3d}".format(mapa[i][j]), end='')
            print()
        print()





        


