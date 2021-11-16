from tabulate import tabulate


def format_solutions(res):

    rows = []
    headers = ["ORIGINE", "DESTINAZIONE", "ORA", "PREZZO", "DURATA", "CAMBI", "TIPO TRENO"]
    for sol in res:
        train_type = sol['trainlist'][0]['trainacronym']
        sol.pop('saleable')
        sol.pop('trainlist')
        tmp = list(sol.values())
        tmp.append(train_type)
        rows.append(tmp)
    print(tabulate(rows, headers))
