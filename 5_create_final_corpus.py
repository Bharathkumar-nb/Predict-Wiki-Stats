import json

dump_folder = './Dumps'

semi_final_dataset_file = dump_folder + '/' + 'semi_final_dataset.dmp'
final_corpus_file = dump_folder + '/' + 'final_corpus.dmp'

with open(final_corpus_file,'w') as final_corpus:
    final_corpus.write('')

with open(semi_final_dataset_file, 'r', encoding='UTF-8') as semi_final_dataset:
    with open(final_corpus_file, 'a', encoding='UTF-8') as final_corpus:
        for line in semi_final_dataset:
            articles = json.loads(line)
            final_corpus.write(articles['news']+'\n')
            final_corpus.write(articles['wiki']+'\n')