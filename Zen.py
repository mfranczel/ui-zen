import time

import numpy
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton
from Populacia import Populacia
import matplotlib.pyplot as plt

gui_kamene = []

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal(str)

    #state 1 - empty
    #state 2 - rock

    def __init__(self):
        self.state = 1
        super(ClickableLabel, self).__init__()
        pixmap = QtGui.QPixmap('imgs/empty_slot.png')
        self.setPixmap(pixmap)

    def flip_state(self):
        if self.state == 1:
            pixmap = QtGui.QPixmap('imgs/rock.png')
            self.setPixmap(pixmap)
            self.state = 2
        else:
            pixmap = QtGui.QPixmap('imgs/empty_slot.png')
            self.setPixmap(pixmap)
            self.state = 1

    def mousePressEvent(self, event):
        self.flip_state()


class Window(QtWidgets.QWidget):
    def __init__(self, width, height):
        QtWidgets.QWidget.__init__(self)
        h_layout = QHBoxLayout(self)
        v_layout = QVBoxLayout()
        self.g_layout = QGridLayout()
        self.g_layout.setSpacing(0)
        h_layout.addLayout(self.g_layout)
        h_layout.addLayout(v_layout)

        go_button = QPushButton('Go!')

        v_layout.addWidget(go_button)
        go_button.clicked.connect(self.handle_go_button)
        self.buttons = []
        self.g_height = height
        self.g_width = width

        for row in range(height):
            buttons_row = []
            for column in range(width):
                label = ClickableLabel()
                self.g_layout.addWidget(label, row, column)
                buttons_row.append(label)
            self.buttons.append(buttons_row)



    def handle_go_button(self):
        global gui_kamene
        gui_kamene = []
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                if self.buttons[i][j].state == 2:
                    kamen = [j,i]
                    gui_kamene.append(kamen)
        self.close()

def plot(xxx, yyy, labely):


    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')
    num = 0
    for xx in xxx:
        plt.plot(xx, yyy[num], marker='', color=palette(num), linewidth=1, alpha=0.9, label=labely[num])
        num += 1


    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


    plt.title("Average fitness per generation", loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel("Generation")
    plt.ylabel("Average fitness")
    plt.show()

def make_conf_with_window(sirka, vyska):
    import sys

    app = QApplication(sys.argv)
    window = Window(sirka, vyska)
    window.setGeometry(500, 300, 200, 200)
    window.show()
    app.exec_()

def main():

    from random import randint
    import conf

    # prekazky vo vzorovom priklade
    prekazky_z = [[1, 2], [2, 4], [4, 3], [5, 1], [8, 6], [9, 6]]

    print("Mozne prikazy:")
    print("\'v\' - vzorova konfiguracia")
    print("\'n\' - nova konfiguracia")
    print("\'i\' - ine")
    vybrane = input("Prikaz: ")
    print()

    if vybrane == "v":
        configs = conf.conf_1
        conf.sirka = 12
        conf.vyska = 10
        conf.runs = 1
    elif vybrane == "n":
        sirka = int(input("sirka: "))
        vyska = int(input("vyska: "))
        make_conf_with_window(sirka, vyska)
        configs = conf.conf_1
        conf.sirka = sirka
        conf.vyska = vyska
        conf.runs = 1

    #configs = conf.configs_mid_pop_test_random_crossover_roulette

    labely = []
    for i in configs:
        labely.append(i[6])

    xxx = []
    yyy = []
    casy = []
    yyyy = []
    xxxx = []

    for config in configs:
        velkost_populacie = config[1]
        pocet_generacii = config[2]
        mutacia = config[0]
        odrez = False
        nahodne_krizenie = config[3]
        elitarizmus = config[4]
        ruleta = config[5]

        for i in range(conf.runs):

            # vygenerovanie prekazok alebo listov podla konfiguracneho suboru
            prekazky = []
            listy = {
                'z': [],
                'o': [],
                'c': []
            }

            for i in range(conf.pocet_prekazok):
                prekazky.append([randint(0, conf.sirka - 1), randint(0, conf.vyska - 1)])

            for i in range(conf.zlte_listy):
                list = [randint(0, conf.sirka - 1), randint(0, conf.vyska - 1)]
                if list not in listy['z'] and list not in prekazky:
                    listy['z'].append([randint(0, conf.sirka - 1), randint(0, conf.vyska - 1)])
                else:
                    i -= 1

            for i in range(conf.oranzove_listy):
                list = [randint(0, conf.sirka - 1), randint(0, conf.vyska - 1)]
                if list not in listy['o'] and list not in prekazky and list not in listy['z']:
                    listy['o'].append([randint(0, conf.sirka - 1), randint(0, conf.vyska - 1)])
                else:
                    i -= 1

            for i in range(conf.cervene_listy):
                list = [randint(0, conf.sirka - 1), randint(0, conf.vyska - 1)]
                if list not in listy['c'] and list not in prekazky and list not in listy['z'] and list not in listy['o']:
                    listy['c'].append([randint(0, conf.sirka - 1), randint(0, conf.vyska - 1)])
                else:
                    i -= 1

            # v pripade, ze su poskytnute lokacie prekazok, treba vyuzit
            if vybrane == "v":
                prek = prekazky_z
            elif vybrane == "n":
                prek = gui_kamene
            else:
                prek = prekazky

            xx = []
            yy = []
            prirastky = []

            #vytvori sa nova populacia
            pop = Populacia(velkost_populacie, conf.sirka, conf.vyska, prek, mutacia, listy)
            for i in range(pocet_generacii):
                start_time = time.time()

                pop.vytvor_novu_populaciu(elitarizmus=elitarizmus, nahodne_krizenie=nahodne_krizenie, ruleta=ruleta)

                xx.append(i)
                yy.append(pop.avg)

                # ak je nastavene orezavanie, v pripade dlhodobeho prilis maleho rastu fitness sa automaticky zastavi
                if odrez:
                    if i > 0:
                        prirastky.append(pop.avg-yy[i-1])
                    else:
                        prirastky.append(pop.avg)

                    print(prirastky[len(prirastky)-1])
                    if len(prirastky)>int(pocet_generacii/10) and numpy.average(prirastky[len(prirastky)-int(pocet_generacii/10):]) < yy[i]/10000:
                        print("stopped after ", i, " generations")
                        break
                else:
                    # ak je nastaveny vypis, vypisuje sa priemerna fitness kazdej generacie
                    if conf.vypis:
                        print("generacia: ", i, " | avg. fitness: ", pop.avg)

            fitness_zoradene = sorted(pop.fitness_populacie.items(), key=lambda x: x[1], reverse=True)
            fitness_zoradene[0][0].vypis_mapu()
            xxx += xx
            yyy.append(yy)
            casy.append(time.time()-start_time)

        yyyy.append(numpy.mean(yyy, axis=0).tolist())
        xxxx.append(numpy.unique(xxx).tolist())

    if vybrane != "v" and vybrane != "n":
        print(casy)
        plot(xxxx, yyyy, labely)


main()
