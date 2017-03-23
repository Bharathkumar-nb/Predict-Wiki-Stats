import json

news_dump_file = '2015-07-01to2017-03-18.dmp'

corpus_file = 'corpus.dmp'

with open(news_dump_file, 'r') as news_dump:
    for day_line in news_dump:
        daily_articles = json.loads(day_line)
        for articles in daily_articles["response"]["results"]:
            with open(corpus_file, 'a', encoding='UTF-8') as corpus:
                corpus.write(articles["fields"]["bodyText"])
                corpus.write('\n')