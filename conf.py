

sirka = 20
vyska = 15
pocet_prekazok = 15
zlte_listy = 0
oranzove_listy = 0
cervene_listy = 0
vypis = False
runs = 50
# pravdepodobnost mutacie, populacia, generacie,
# nahodne_krizenie, elitarizmus, ruleta, graf label

configs_mid_pop = [
        [2, 50, 100, False, True, True, "50 pop., 100 gen."],
        [2, 100, 100, False, True, True, "100 pop., 100 gen."],
        [2, 200, 100, False, True, True, "200 pop., 100 gen."],
        [2, 350, 100, False, True, True, "350 pop., 100 gen."],
]

configs_mid_pop_high_mutation = [
        [5, 50, 100, False, True, True, "50 pop., 100 gen."],
        [5, 100, 100, False, True, True, "100 pop., 100 gen."],
        [5, 200, 100, False, True, True, "200 pop., 100 gen."],
        [5, 350, 100, False, True, True, "350 pop., 100 gen."],
]

configs_mid_pop_test_mutation = [
        [2, 200, 100, False, True, True, "200 pop., 100 gen."],
        [5, 200, 100, False, True, True, "200 pop., 100 gen."],
        [10, 200, 100, False, True, True, "200 pop., 100 gen."],
]

configs_mid_pop_test_random_crossover = [
        [5, 200, 100, True, True, True, "náhodné kríženie"],
        [5, 200, 100, False, True, True, "50:50 kríženie"],
]

configs_mid_pop_test_random_crossover_no_elitarizm = [
        [5, 200, 100, True, True, True, "S elitarizmom"],
        [5, 200, 100, True, False, True, "Bez elitarizmu"],
]

configs_mid_pop_test_random_crossover_roulette = [
        [5, 200, 100, True, True, True, "S ruletou"],
        [5, 200, 100, True, False, False, "S turnajom"],
]

conf_1 = [[5, 200, 100, True, True, False, ""]]

