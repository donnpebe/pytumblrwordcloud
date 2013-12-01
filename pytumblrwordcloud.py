import requests
import mlstripper as ml
from collections import Counter
from pytagcloud import create_tag_image, make_tags, LAYOUTS
import json

f = open('info.json')
config = json.load(f)
f.close()

url = 'http://api.tumblr.com/v2/blog/{0}/posts/text?api_key={1}'.format(
    config['BASE_HOSTNAME'],config['API_KEY'])
punctuation = "!\"\n\xc2\xa0$%&'()*+,-./:;<=>?[\]^_`{|}~'"
max_word_size = 60
max_words = 60
width = 950
height = 450
background_color = (22, 22, 22)
layout = 3

f = open('excludewords.txt', 'rb')
stop_words = [line.strip() for line in f]
f.close();

r = requests.get(url)
posts = r.json()

all_text = ''
for text in posts['response']['posts'] :
    content = ml.strip_tags(text['body']).encode('utf-8').lower()
    filtered_content = ""
    for ch in content :
        if ch not in punctuation :
            filtered_content += ch
        else:
            filtered_content += " "
    all_text += filtered_content

words = all_text.split()
counts = Counter(words)
for word in stop_words:
    del counts[word]

words_to_use = counts.most_common(max_words)
tags = make_tags(words_to_use, maxsize=max_word_size)

create_tag_image(tags, 'word_cloud.png', size=(width, height), layout=layout, 
    fontname='Lobster', background = background_color)    
print "Word cloud created. Good Job!"
