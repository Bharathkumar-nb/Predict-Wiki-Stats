import json
import importlib.util
from datetime import date
from dateutil.rrule import rrule, DAILY
spec = importlib.util.spec_from_file_location("Content", "./theguardian-api-python/theguardian/theguardian_content.py")
theguardian_content = importlib.util.module_from_spec(spec)
spec.loader.exec_module(theguardian_content)

start_date = date(2015,7,1)
end_date = date.today()

dump_folder = './Dumps'

if not os.path.exists(dump_folder):
    os.mkdir(dump_folder)


dump_filename = dump_folder + '/' + date.strftime(start_date,"%Y-%m-%d")+'to'+date.strftime(end_date,"%Y-%m-%d")+'.dmp'

with open(dump_filename, 'w') as outfile:
    outfile.write('')


no_of_days = 0
for dt in rrule(DAILY, dtstart=start_date, until=end_date):
    
    headers = {"from-date":dt.strftime("%Y-%m-%d"), "to-date":dt.strftime("%Y-%m-%d"), "show-fields":"headline,trailText,newspaperPageNumber,wordcount,publication,firstPublicationDate,bodyText,", "page-size":"10"}

    content = theguardian_content.Content(api='test',**headers)

    raw_content = content.get_request_response()
    if raw_content.status_code != 200:
        print('Error while retrieving articles on date: ', dt.strftime("%Y-%m-%d"))
        continue

    # get all results of a page
    json_content = content.get_content_response()
    all_results = content.get_results(json_content)

    with open(dump_filename, 'a') as outfile:
        outfile.write(json.dumps(json_content)+'\n')

    no_of_days += 1
    print('Days processed: ', no_of_days)

print('Total number of Days processed: ', no_of_days)