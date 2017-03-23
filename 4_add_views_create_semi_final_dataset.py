import json
from datetime import datetime
from mwviews.api import PageviewsClient

dump_folder = './Dumps'

dataset_file = dump_folder + '/' + 'dataset.dmp'
stats_file = dump_folder + '/' + 'stats.txt'
semi_final_dataset_file = dump_folder + '/' + 'semi_final_dataset.dmp'

p = PageviewsClient()

i=0

with open(semi_final_dataset_file, 'w') as semi_final_dataset:
    semi_final_dataset.write('')

with open(dataset_file, 'r') as dataset:
    with open(stats_file, 'r') as stats:
        with open(semi_final_dataset_file, 'a') as semi_final_dataset:
            statistics = stats.readlines()
            statistics = [s for s in statistics if 'ERRORFAIL' not in s]
            current_stat_read_line = 0
            previous_date = None
            data_out = []
            stat_out = []
            for data in dataset:
                data_dic = json.loads(data)
                stat_dic = json.loads(statistics[current_stat_read_line])
                current_stat_read_line += 1
                current_date = data_dic['webPublicationDate'].split('T')[0].replace('-','')

                if previous_date == None or previous_date==current_date:
                    if previous_date == None:
                        previous_date = current_date
                    data_out.append(data_dic)
                    stat_out.append(stat_dic)
                else:
                    articles = [dic['wiki_link'].split('/')[-1] for dic in stat_out]
                    views = p.article_views('en.wikipedia', articles, granularity='daily',  start=previous_date, end=previous_date)
                    for d_dic,s_dic in zip(data_out,stat_out):
                        d_dic['views'] = views[datetime.strptime(previous_date, "%Y%m%d")][s_dic['wiki_link'].split('/')[-1]]
                        if d_dic['views'] == None:
                            d_dic['views'] = 0
                        i+=1
                        print('Writing file: ', i)
                        semi_final_dataset.write(json.dumps(d_dic) + '\n')
                    data_out = [data_dic]
                    stat_out = [stat_dic]
                    previous_date = current_date
            if len(stat_out) > 0:
                articles = [dic['wiki_link'].split('/')[-1] for dic in stat_out]
                views = p.article_views('en.wikipedia', articles, granularity='daily',  start=previous_date, end=previous_date)
                for d_dic,s_dic in zip(data_out,stat_out):
                    d_dic['views'] = views[datetime.strptime(previous_date, "%Y%m%d")][s_dic['wiki_link'].split('/')[-1]]
                    if d_dic['views'] == None:
                        d_dic['views'] = 0
                    i+=1
                    print('Writing file: ', i)
                    semi_final_dataset.write(json.dumps(d_dic) + '\n')