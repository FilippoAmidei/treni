def filter_results_by_maxprice(res, price):
    tmp = []
    for x in res:
        tmp = tmp + x
    tmp = [d for d in tmp if d['minprice'] < price]
    return tmp


def filter_results_by_number(res, n_results):
    tmp = []
    for x in res:
        tmp = tmp + x
    tmp = sorted(tmp, key=lambda d: d['minprice'])
    return tmp[:n_results]


def filter_results_by_params(res, price=None, n_changes=None, train_type=None):  # kwargs = price, n_changes, train_type

    tmp = []
    for x in res:
        tmp = tmp + x
    if price is not None:
        tmp = [d for d in tmp if d['minprice'] < price]
    if n_changes is not None:
        tmp = [d for d in tmp if d['changesno'] <= n_changes]
    if train_type is not None and n_changes == 0:
        tmp = [d for d in tmp if d['trainlist'][0]['trainacronym'] == train_type]
    return tmp
