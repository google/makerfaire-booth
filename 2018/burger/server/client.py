import pandas
import requests

burgers = pandas.read_hdf('split.h5', 'train')

def do_request():
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
        if r2.status_code == 200:
            r3 = requests.get('http://gork:8888/validate')
            print(r3.status_code)
            if r3.status_code == 200:
                print(r3.text)
                response = r3.json()
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
        else:
            print("Failed:",r2.status_code,r2.text)
def main():
    while True:
        do_request()

if __name__ == '__main__':
    main()
