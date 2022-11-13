import json
import re

result=open("result.txt")
database=[]
class Tweet:
    def __init__(self,author_id,created_at,edit_history_tweet_ids,geo,id,lang,text):
        self.author_id=author_id
        self.created_at=created_at
        self.edit_history_tweet_ids=edit_history_tweet_ids
        self.geo=geo
        self.id=id
        self.lang=lang
        self.text=text
        string=self.text
        string=re.sub(r'[,.?!…]',"",string)
        #string = re.sub(r'@[A-Za-z0-9]*', "", string)
        string = re.sub(r'RT', "", string)
        string = re.sub(r'https:\/\/.*? ', "", string)
        string = re.sub(r'https:\/\/.*?$', "", string)
        string = re.sub(r'\n', "", string)
        string = re.sub(r'["\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF"]', " \0", string)
        string = re.sub(r'[:;]', "", string)
        wordList=string.split(" ")
        self.words=[]
        for word in wordList:
            if word != "":
                self.words.append(word)

for data in result:
    data=json.loads(data)
    record=Tweet(data.get("author_id"),data.get("created_at"),data.get("edit_history_tweet_ids"),data.get("geo"),data.get("id"),data.get("lang"),data.get("text"))
    database.append(record)

