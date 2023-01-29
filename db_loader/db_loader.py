import json
from elasticsearch import Elasticsearch

file_name = '/home/idykyi/programming/bible/json/en_kjv.json'
es = Elasticsearch(hosts=[{'host': "localhost", 'port': 9200, "scheme": "http"}])

if __name__ == '__main__':
    with open(file_name, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
        for book in data:
            for idx, chapter in enumerate(book['chapters']):
                chapter = "".join([str(index+1) + " " + chapter[index] for index in range(0, len(chapter))])
                doc = {
                    'book': book['name'],
                    'chapter': idx+1,
                    'text': chapter
                }
                print(book['name'], idx+1)
                resp = es.index(index="bible-3", document=doc)
