from help_json import *
from partitioner import Partitioner
import argparse

def remove_if_necessary(partition, element):
    if element in partition:
        partition.remove(t)
        return True
    return False

def create_arguments():
   parser = argparse.ArgumentParser()

   parser.add_argument('-small_split')
   parser.add_argument('-full_split')
   parser.add_argument('-full_data')
   parser.add_argument('-len_val', default = 20, type = int)
   parser.add_argument('-file_destiny', default = 'split_full_test_small.json')   

   return parser.parse_args()


args = create_arguments()

small   = get_json(args.small_split)
full    = get_json(args.full_split)

full['train'] = full['train'] + full['test']
full['test']  = small['test']

for t in full['test']:
    if remove_if_necessary(full['val'], t):
        full['val'].append(full['train'].pop(0))
    else:
        remove_if_necessary(full['train'], t)

assert len([i for i in full['train'] if i in full['test'] + full['val']]) == 0, 'Treinamento presente em validação ou teste'
assert len([i for i in full['test']  if i in full['val'] + full['train']]) == 0, 'Teste presente em validação ou treinamento'
assert len([i for i in full['val']   if i in full['test'] + full['train']]) == 0, 'Validação presente em teste ou treinamento'

refexps = get_json(args.full_data)
refexps = [r for r in refexps if r['id'] not in full['test']]

partitioner = Partitioner()
dataset = partitioner.partition(refexps, percentage_validacao = args.len_val, percentage_teste = 0)
dataset['test'] = full['test']

assert len([i for i in dataset['train'] if i in dataset['test'] + dataset['val']]) == 0, 'Treinamento presente em validação ou teste'
assert len([i for i in dataset['test']  if i in dataset['val']  + dataset['train']]) == 0, 'Teste presente em validação ou treinamento'
assert len([i for i in dataset['val']   if i in dataset['test'] + dataset['train']]) == 0, 'Validação presente em teste ou treinamento'
assert len([i for i in dataset['test']  if i in small['test']]) == len(set(dataset['test'])), 'Erro ao copiar exemplos de treinamento'

total_len = len(dataset['train'] + dataset['test'] + dataset['val'])

save_json(args.file_destiny, dataset)

print('{} exemplos de treinamento ({} )'.format(len(dataset['train']), (len(dataset['train']) * 100 / total_len)))
print('{} exemplos de validação ({} )'.format(len(dataset['val']), (len(dataset['val']) * 100 / total_len)))
print('{} exemplos de teste ({} )'.format(len(dataset['test']), (len(dataset['test']) * 100 / total_len)))

#python3 full_to_small_dataset.py -small_split ../Split-Small-To-Full/split_anon_small.json -full_split ../Split-Small-To-Full/split_images.json -full_data ../../google_refexp_phrase.json -len_val 20