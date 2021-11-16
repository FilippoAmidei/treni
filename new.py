import urllib.parse
from datetime import datetime, timedelta
import copy
from concurrent import futures
import requests
from timeit import default_timer as timer
from filters import *
from format_solutions import format_solutions

def solutions_5(response):
    response_json = response.json()
    wanted_keys = ['origin', 'destination', 'departuretime', 'minprice', 'duration', 'changesno', 'saleable', 'trainlist']
    result_list = []
    for x in response_json:
        t = x['departuretime']
        conv_t = datetime.fromtimestamp(t/1000).strftime('%d-%m-%Y %H:%M')
        x.update(departuretime=conv_t)
        result_list.append({k: x[k] for k in wanted_keys})
    return result_list


def generate_payloads(init_payload, end_date):
    payload = init_payload
    payloads_results = []
    datetimeEndDate = datetime.strptime(end_date, '%d/%m/%Y')
    while True:
        payloads_results.append(copy.deepcopy(payload))
        tmp = payload['adate']
        new_date = datetime.strptime(tmp, '%d/%m/%Y')
        new_date = new_date + timedelta(days=1)
        if new_date > datetimeEndDate:
            break
        new_date = new_date.strftime('%d/%m/%Y')
        payload.update(adate=new_date)
    return payloads_results

def solutions_one_day(init_payload, session):

    payload = init_payload
    payload.update(offset=0)
    results = []
    while True:
        t = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote, safe='/')
        res = session.get('https://www.lefrecce.it/msite/api/solutions', params=t)
        if res.text == '[]':
            break
        results = results + solutions_5(res)
        tmp = payload['offset']
        tmp = str(int(tmp) + 5)
        payload.update(offset=tmp)
    return results

payload = {
    'origin': 'FIRENZE ( TUTTE LE STAZIONI )',
    'destination': 'MILANO ( TUTTE LE STAZIONI )',
    'arflag': 'A',
    'adate': '26/11/2021',
    'atime': '01',
    'adultno': '1',
    'childno': '0',
    'direction': 'A',
    'frecce': 'false',
    'onlyRegional': 'false',
    'offset': '0'
}
start = timer()
a = generate_payloads(payload, '10/12/2021')
s = requests.Session()
pool = futures.ThreadPoolExecutor(max_workers=20)
results = []
for res in pool.map(lambda p: solutions_one_day(p, s), a):
    results.append(res)
end = timer() - start
print(end)
b = filter_results_by_params(results, 25, 0, 'IC')
format_solutions(b)

#print(a)