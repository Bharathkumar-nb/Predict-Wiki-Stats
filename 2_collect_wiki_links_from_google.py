import json
import time
from googleapiclient.discovery import build

dump_folder = './Dumps'

dump_file = dump_folder + '/' + '2015-07-01to2017-03-18.dmp'

wiki_map_path = dump_folder + '/' + 'wiki_map.dmp'
wiki_map_full_path = dump_folder + '/' + 'wiki_map_full.dmp'

no_queries = 0
no_lines = 0
no_empty_results = 0

developerKey = ''
cx = ''

with open('keys.txt', 'r') as key_file:
    dic = json.load(key_file)
    key = dic['key']
    se = dic['search_engine']

service = build("customsearch", "v1", developerKey=key)

with open(dump_file, 'r') as f:
    for day_line in f:
        daily_articles = json.loads(day_line)
        no_lines += 1
        print("Reading line: ", no_lines)
        if no_lines<=340:
            continue
        #print(list(daily_articles.keys()))
        article_2_wiki_map = {}
        article_2_wiki_map_full = {}
        
        for article in daily_articles['response']['results']:
            #print(article['fields']['headline'] == '')
            res = service.cse().list(q=article['fields']['headline']+' wikipedia',cx=se).execute()
            #print(res)
            article_2_wiki_map_full[article["apiUrl"]] = res
            #print(article_2_wiki_map)
            if res['searchInformation']['totalResults'] != '0':
                article_2_wiki_map[article["apiUrl"]] = [item['link'] for item in res['items']]
            else:
                print('Query returned empty result')
                no_empty_results += 1
            #print(article_2_wiki_map)
            #print()
            no_queries += 1
            print('processing query: ', no_queries)
            if no_queries%5 == 0:
                time.sleep(3)

        with open(wiki_map_path, 'a') as wiki_map_outfile:
            wiki_map_outfile.write(json.dumps(article_2_wiki_map)+'\n')
        with open(wiki_map_full_path, 'a') as wiki_map_full_outfile:
            wiki_map_full_outfile.write(json.dumps(article_2_wiki_map_full)+'\n')

        # if no_queries > 2:
        #     break
print('Total number of lines: ', no_lines)
print('Total number of queries: ', no_queries)
print('Total number of empties: ', no_empty_results)

# f.close()
# wiki_map_outfile.close()
# wiki_map_full_outfile.close()