import json
import wikipedia
import time

dump_folder = './Dumps'

news_dump_file = dump_folder + '/' + '2015-07-01to2017-03-18.dmp'
news_wiki_link_file = dump_folder + '/' + 'wiki_map.dmp'
dataset_file = dump_folder + '/' + 'dataset.dmp'
stats_file = dump_folder + '/' + 'stats.txt'

wikipedia.set_rate_limiting(True)

i=0

with open(dataset_file, 'w') as dataset:
    with open(stats_file, 'a') as stats:
        dataset.write('')
        stats.write('')

with open(news_dump_file, 'r', encoding='UTF-8') as news_dump:
    with open(news_wiki_link_file, 'r') as news_wiki_link:
        with open(dataset_file, 'a') as dataset:
            with open(stats_file, 'a') as stats:
                news_wiki_link_lines = news_wiki_link.readlines()
                current_read_line = -1
                for line in news_dump:
                    daily_articles = json.loads(line)
                    current_read_line += 1
                    for article in daily_articles['response']['results']:
                        news_wiki_map = json.loads(news_wiki_link_lines[current_read_line])
                        if(article['apiUrl'] in news_wiki_map):
                            for wiki_link in news_wiki_map[article["apiUrl"]]:
                                stats_map = {}
                                stats_map['apiUrl'] = article['apiUrl']
                                stats_map['wiki_link'] = wiki_link
                                try:
                                    page = wikipedia.page(wiki_link.split('/')[-1], auto_suggest=True)
                                    dataset_line = {}
                                    dataset_line["sectionId"] = article["sectionId"]
                                    dataset_line["type"] = article["type"]
                                    dataset_line["webPublicationDate"] = article["webPublicationDate"]
                                    dataset_line["wordcount"] = article['fields']["wordcount"]
                                    dataset_line['news'] = article['fields']["bodyText"].replace('\n',' ')
                                    dataset_line['wiki'] = page.content.replace('\n',' ')
                                    stats_map['status'] = '200OK'

                                    dataset.write(json.dumps(dataset_line)+'\n')

                                except Exception as e:
                                    stats_map['status'] = 'ERRORFAIL'
                                    print(e)
                                    pass
                                stats.write(json.dumps(stats_map)+'\n')
                                i+=1
                                print(i)