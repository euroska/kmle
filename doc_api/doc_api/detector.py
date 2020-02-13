from tika import parser
from dateutil.parser import parse
import requests

#with open('./examples/doc.docx', 'rb') as f:
    #data = f.read()
    #parsed = parser.from_buffer(data)
    #print(parsed)

#parsed = parser.from_file('./examples/doc.docx', service='meta')

with open('./examples/doc.docx', 'rb') as f:
    r = requests.put(
        'http://172.17.0.7:9998/meta',
        data=f.read(),
        headers={
            'Accept': 'application/json',
        }
    )
    parsed = r.json()

    print(parsed)
    metadata = {
        'author': parsed['Author'],
        'time_of_creation': parse(parsed['Creation-Date']),
        'word_count': parsed['meta:word-count'],
        'language': parsed['language'],
    }
    print('-' * 64)
    print(metadata)
