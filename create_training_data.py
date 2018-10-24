import sqlite3
import pandas as pd

timeframes = ['2008-04']

for timeframe in timeframes:
    connection = sqlite3.connect('{}.db'.format(timeframe))
    c = connection.cursor()
    limit = 5000            #amount to pull and throw into dataframe
    last_unix = 0           #buffer through dataframe
    cur_length = limit
    counter = 0
    test_done = False
    while cur_length == limit:
        df = pd.read_sql("SELECT * FROM parent_reply WHERE unix > {} AND parent NOT NULL AND score > 0  ORDER BY unix ASC LIMIT {}".format(last_unix,limit), connection)
        last_unix = df.tail(1)['unix'].values[0]
        cur_length = len(df)
        if not test_done:   
            with open("test.from",'a',encoding='utf8') as f:
                for content in df['parent'].values:
                    f.write(content+'\n')
            with open("test.to",'a',encoding='utf8') as f:
                for content in df['comment'].values:
                    f.write(content+'\n')
            test_done = True
        else:
            with open("train.from",'a',encoding='utf8') as f:
                for content in df['parent'].values:
                    f.write(content+'\n')
            with open("train.to",'a',encoding='utf8') as f:
                for content in df['comment'].values:
                    f.write(content+'\n')
            test_done = True
        counter +=1
        if counter % 10 == 0:
            print(counter*limit,"Rows completed so far..")

