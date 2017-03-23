with open('2015-07-01to2017-03-18.dmp','r',encoding='UTF-8') as f1:
    with open('wiki_map.dmp','r') as f2:
        i = 1
        j = 1

        for line in f1:
            with open('dumps/news'+str(j)+'.dmp','a') as f3:
                f3.write(line)
            if i%60 == 0:
                j+=1
            i+=1

        i = 1
        j = 1

        for line in f2:
            with open('dumps/wiki'+str(j)+'.dmp','a') as f3:
                f3.write(line)
            if i%60 == 0:
                j+=1
            i+=1
        