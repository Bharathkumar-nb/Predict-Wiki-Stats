import json
import wikipedia
import time

dump_folder = './Dumps'

wiki_map_file = dump_folder + '/' + 'wiki_map.dmp'
corpus_file = dump_folder + '/' + 'wiki_corpus.dmp'

num_links = 0
num_error_links = 0

wikipedia.set_rate_limiting(True)

with open(wiki_map_file, 'r', encoding='UTF-8') as wiki_map:
    for day_line in wiki_map:
        daily_articles = json.loads(day_line)
        for k, wiki_links in daily_articles.items():
            for link in wiki_links:
                try:
                    page = wikipedia.page(link.split('/')[-1], auto_suggest=True)
                    num_links += 1
                    print('Links processed: ', num_links)
                    with open(corpus_file, 'a', encoding='UTF-8') as corpus:
                        corpus.write(page.content.replace('\n',' '))
                        corpus.write('\n')
                except Exception as e:
                    num_error_links += 1
                    print('Error occured')
                    pass
            time.sleep(3)

print('Total Links processed: ', num_links)
print('Number of error links: ', num_error_links)