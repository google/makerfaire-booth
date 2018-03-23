import operator
import collections
import pandas
import itertools
from enum import Enum, unique

from constants import MAX_BURGER_HEIGHT, column_names
from burger_elements import BurgerElement
from label_burger import label_burger
from burger_features import has_sequential_nonempty_duplicates, has_internal_or_terminal_empty, has_patty_under_last_cheese, has_internal_bun, empty_prefix_count, empty_topbun_prefix, count

def burger_to_index(burger):
    return ''.join([str(layer) for layer in burger])

def index_to_burger(index):
    return [int(layer) for layer in list(index)]



names = [member.name for member in BurgerElement.__members__.values()]
values = [member.value for member in BurgerElement.__members__.values()]
burgers_it = itertools.product(values, repeat=MAX_BURGER_HEIGHT)
burgers = list(burgers_it)
index = [burger_to_index(burger) for burger in burgers]
df = pandas.DataFrame(data=burgers,
                      columns = column_names,
                      index=index)

labels = [label_burger(burger) for burger in burgers]
df['output'] = labels
df.to_csv('data.csv', index_label='id')

#TODO(dek): put this in burger_features
c = dict([(burger, count(burger)) for burger in burgers])
topbun_getter = operator.itemgetter(BurgerElement.topbun.value)
bottombun_getter = operator.itemgetter(BurgerElement.bottombun.value)
patty_getter = operator.itemgetter(BurgerElement.patty.value)
df['has_sequential_nonempty_duplicates'] = [has_sequential_nonempty_duplicates(burger) for burger in burgers]
df['has_internal_or_terminal_empty'] = [has_internal_or_terminal_empty(burger) for burger in burgers]
df['has_patty_under_last_cheese'] = [has_patty_under_last_cheese(burger) for burger in burgers]
df['has_internal_bun'] = [has_internal_bun(burger) for burger in burgers]
df['empty_prefix_count'] = [empty_prefix_count(burger) for burger in burgers]
df['empty_topbun_prefix'] = [empty_topbun_prefix(burger) for burger in burgers]
df['topbun_count'] = [topbun_getter(c[burger]) for burger in burgers]
df['bottombun_count'] = [bottombun_getter(c[burger]) for burger in burgers]
df['patty_count'] = [patty_getter(c[burger]) for burger in burgers]

df.to_hdf('data.h5', 'df', format='fixed')
