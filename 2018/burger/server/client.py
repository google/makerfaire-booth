import pandas
import requests

burgers = pandas.read_hdf('../machine/data.h5', 'df')

while True:
    r = requests.get('http://gork:8888/burger')
    if r.status_code == 200:
        j = r.json()
        burger = j['burger']
        print(burger)
        burger = ''.join([str(layer) for layer in burger])
        vote = burgers.loc[burger].output
        print(vote)
        r2 = requests.get('http://gork:8888/vote?vote=%s&burger=%s' % (vote, burger))
        print(r2.status_code)
        print(r2.text)
        response = r2.json()
        print(response['burger'])
        print(response['classification_report'])
        tp = response["tp"]
        fp = response["fp"]
        tn = response["tn"]
        fn = response["fn"]

        print("TP:", tp)
        print("FP:", fp)
        print("TN:", tn)
        print("FN:", fn)
        print("FPR:", fp/float(fp+tn))
        print("FNR:", fn/float(fn+tp))

