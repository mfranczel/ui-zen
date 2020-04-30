from Jedinec import Jedinec
from random import randint

class Populacia:

    pop = []

    def __init__(self, velkost_populacie, sirka, vyska, prekazky, pravdepodobnost_mutacie, listy=None):
        #nastavia sa parametre
        self.velkost_populacie = velkost_populacie
        self.sirka = sirka
        self.vyska = vyska
        self.prekazky = prekazky
        self.pravdepodobnost_mutacie = pravdepodobnost_mutacie
        self.listy = listy

        # pri inicializacii sa vytvori nova populacia jedincov
        for i in range(velkost_populacie):
            jedinec = Jedinec(sirka,vyska,prekazky,listy=listy)
            jedinec.generuj_nahodne_geny()
            self.pop.append(jedinec)


    def vypocitaj_fitness_populacie(self):
        #vypocita sa fitness populacie pre kazdeho jedinca a zaroven aj celkova fitness
        celkova_fitness = 0
        fitness_mapa = {}
        for jedinec in self.pop:
            celkova_fitness += jedinec.fitness

        for jedinec in self.pop:
            fitness_mapa[jedinec] = jedinec.fitness

        self.fitness_populacie = fitness_mapa
        self.celkova_fitness = celkova_fitness

        return fitness_mapa


    def vyber_nahodne_ruleta(self):

        # vyberie sa nahodne cislo, scitava sa fitness pokial nie je scitana fitness vacsia ako nahodne cislo
        fitness_zoradene = sorted(self.fitness_populacie.items(), key=lambda x:x[1])
        zatocenie_kolesom = randint(0, self.celkova_fitness)
        parcialna_suma = 0

        for i in fitness_zoradene:

            if zatocenie_kolesom <= parcialna_suma + i[1] and parcialna_suma < zatocenie_kolesom:
                return i[0]
            parcialna_suma += i[1]

        return fitness_zoradene[len(fitness_zoradene)-1][0]

    def vyber_nahodne_turnaj(self, velkost):
        # vytvori sa turnaj velkosti velkost, zoradi sa a vrati sa jedinec s najvyssou fitness
        potencionalny_rodicia = []

        for i in range(velkost):
            potencionalny_rodicia.append(self.pop[randint(0,self.velkost_populacie-1)])

        najlepsi = potencionalny_rodicia[0]

        for i in range(velkost):
            if potencionalny_rodicia[i].fitness > najlepsi.fitness:
                najlepsi = potencionalny_rodicia[i]

        return najlepsi


    def mutacia_v1(self, geny, otec):
        # pri kazdom gene je urcita p mutacie
        for i in range(len(geny)):
            mutacia = randint(0, 100)
            if mutacia < self.pravdepodobnost_mutacie:
                geny[i] = randint(0, 2*otec.sirka + 2*otec.vyska - 1)
        return geny

    def mutacia_v2(self, geny, otec):
        #pri kazdom jedincovi je urcita p mutacie jedneho nahodneho genu
        rand_gen = randint(0, len(geny)-1)

        if randint(0,100) < self.pravdepodobnost_mutacie:
            geny[rand_gen] = randint(0, 2*otec.sirka + 2*otec.vyska - 1)

        return geny


    def skriz(self, otec, mama):
        #skrizia sa geny v pomere 1:1
        leng = len(otec.geny)

        nove_geny = otec.geny[:int(leng/2)] + mama.geny[int(leng/2):]
        nove_geny = self.mutacia_v2(nove_geny, otec)

        novy_jedinec = Jedinec(otec.sirka, otec.vyska, otec.prekazky, self.listy,geny=nove_geny)

        return novy_jedinec

    def skriz_nahodne(self, otec, mama):
        #skrizia sa geny v nahodnom pomere
        leng = len(otec.geny)

        stred = randint(0,leng)

        nove_geny = otec.geny[:int(stred)] + mama.geny[int(stred):]
        nove_geny = self.mutacia_v2(nove_geny, otec)

        novy_jedinec = Jedinec(otec.sirka, otec.vyska, otec.prekazky, self.listy,geny=nove_geny)

        return novy_jedinec

    def vyber_elitu(self, kolko):
        # vyberie sa x jedincov s najvyssim fitness
        fitness_zoradene = sorted(self.fitness_populacie.items(), key=lambda x: x[1], reverse=True)
        elita = []
        for i in range(kolko):
            elita.append(fitness_zoradene[i][0])

        return elita

    def vytvor_novu_populaciu(self, elitarizmus, nahodne_krizenie=False, ruleta=True):
        # vytvori sa nova populacia a vykona sa genocida na starej
        self.vypocitaj_fitness_populacie()
        self.avg = self.celkova_fitness/len(self.pop)
        kolko_krizit = self.velkost_populacie

        if elitarizmus:
            nova_pop = self.vyber_elitu(int(self.velkost_populacie/5))
            kolko_krizit -= int(self.velkost_populacie/5)
        else:
            nova_pop = []

        for i in range(kolko_krizit):
            if ruleta:
                otec = self.vyber_nahodne_ruleta()
                mama = self.vyber_nahodne_ruleta()
            else:
                otec = self.vyber_nahodne_turnaj(3)
                mama = self.vyber_nahodne_turnaj(3)

            if nahodne_krizenie:
                nova_pop.append(self.skriz_nahodne(otec, mama))
            else:
                nova_pop.append(self.skriz(otec,mama))

        self.pop = nova_pop
