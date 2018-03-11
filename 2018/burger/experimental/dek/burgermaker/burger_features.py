import msgpack
import pandas
import sys
sys.path.insert(0, "../burgerdata")
from burger_data import BurgerElement



# def featurize_burger(burger):
#     import time
#     t0 = time.time()
#     vc = burger.value_counts()
#     burger_no_empties = burger[burger != BurgerElement.empty]
#     features = {
#         'crown_count': vc.get(BurgerElement.crown, 0),
#         'heel_count': vc.get(BurgerElement.heel, 0),
#         'patty_count': vc.get(BurgerElement.patty, 0),
#         # bug: since it works on the filtered list, two non-conseq items sep by an empty will show as seq dupes
#         'non_empty_sequential_duplicates': len(burger_no_empties.loc[burger_no_empties.shift() == burger_no_empties])
#         }
        
#     return features

# def featurize_burgers(burgers):
#     crown_count = []
#     heel_count = []
#     patty_count = []
#     non_empty_sequential_duplicates = []
#     for index, burger in burgers.iterrows():
#         print index
#         features = featurize_burger(burger)
#         print burger, features
#     crown_count.append(features['crown_count'])
#     heel_count.append(features['heel_count'])
#     patty_count.append(features['patty_count'])
#     non_empty_sequential_duplicates.append(features['non_empty_sequential_duplicates'])
        
#     empty_prefix = df.layer1 == BurgerElement.empty
#     crown_prefix = df.layer1 == BurgerElement.crown
#     heel_suffix = df.layer8 == BurgerElement.heel

#     # df['single_crown'] = single_crown
#     # df['single_heel'] = single_heel
#     # df['at_least_one_patty'] = at_least_one_patty
#     # df['empty_prefix'] = empty_prefix
#     # df['crown_prefix'] = crown_prefix
#     # df['heel_suffix'] = heel_suffix

r= msgpack.unpackb(open("burger_features.dat").read())
