from sklearn.preprocessing import OneHotEncoder
N_VALUE=10
def get_one_hot():
    enc = OneHotEncoder(n_values=[N_VALUE,N_VALUE,N_VALUE,N_VALUE,N_VALUE,N_VALUE])
    return enc
