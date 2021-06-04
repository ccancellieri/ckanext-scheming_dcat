import pandas as pd
import requests
import json
import sys


def get_vocabulary(file_name):
    df = pd.read_csv(file_name, usecols=['name'])
    tags = df.to_dict(orient='records')
    return tags

def create_vocabulary(url, key, name):
    print('##################')
    print('#################################')
    print('Creating vocabulary')
    data={
          'name': name
      }
    r = requests.post(url + '/api/action/vocabulary_create',
                      data,
                      headers={'Authorization': key})

    if r.status_code != 200:
        print ('Error while adding vocabulary: {0} error = {1}'.format(name, r.content))
    else:
        print ('Vocabulary {0} was successfully created'.format(name))
    return r

def load_vocabulary(url, key, vocabulary_id, tags):
    print('##################')
    print('########################')
    print('Loading tags')
    for tag in tags:
        tag.update({'vocabulary_id': vocabulary_id})
        r = requests.post(url + '/api/action/tag_create',
                          data=tag,
                          headers={'Authorization': key})

        if r.status_code != 200:
            print ('Error while adding tag : {0} error = {1}'.format(tag, r.content))
            return False
        else:
            print ("Tag {0} was successfully created".format(tag))
    return True

def create_and_load_vocabulary(url,key,file_name, vocabulary_name):
    # Can create a vocabulary
    response = create_vocabulary(url, key, vocabulary_name)
    content = json.loads(response.content)
    if response.status_code != 200:
        print('#####################')
        print('Failed to create a vocabulary {0}'.format(vocabulary_name))
        return False
    # Can load tags
    vocabulary_id = content['result']['id']
    tags = get_vocabulary(file_name)
    response = load_vocabulary(url, key, vocabulary_id, tags)

    if not response:
        print('#####################')
        print('Failed to create tags')
        return False

    return True


# Note
# This is the order of the arguments passed from the python script terminal to the function
# url[0], key[1] vocabulary_id[2]

url = sys.argv[1]
key = sys.argv[2]
file_name = sys.argv[3]
vocabulary_name = sys.argv[4]

create_and_load_vocabulary(url, key, file_name, vocabulary_name)
