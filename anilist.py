try:
    import ujson as json
except:
    import json
import re
import requests
import translate


url = 'https://graphql.anilist.co'


def search(name: str, MediaType: str):
    t = {'a': 'ANIME', 'm': 'MANGA'}
    query = '''
    query ($id: Int, $page: Int, $perPage: Int, $search: String) {
        Page (page: $page, perPage: $perPage) {
            media (id: $id, type: ''' + t[MediaType] + ''', search: $search) {
                id
                title {
                    romaji
                }
                format
                coverImage{
                    extraLarge
                }
            }
        }
    }'''

    variables = {
        'search': name,
        'page': 1,
        'perPage': 8,
        'MediaType': MediaType
    }

    try:
        response = requests.post(
        url, json={'query': query, 'variables': variables})
    except Exception as e:
        print('search',e)
        return False
    # print(response.text)
    else:

        if response.status_code==200:
            try:return list(x for x in json.loads(response.text)['data']['Page']['media'])
            except Exception as e:
                print('search',e)
                return False
        else:
            print('search estatus code',response.status_code)
            return False


def get(id):
    query = '''
	query ($id: Int){
	Media (id: $id){
        coverImage{
            extraLarge
        }
		title {
		romaji		
		}
		format
        startDate{
            year
        }
		status
		episodes
		genres
        tags{
            name
        }
		description
	}
	}
	'''

    variables = {
        'id': id
    }


    try:
        # Make the HTTP Api request
        response = requests.post(
            url, json={'query': query, 'variables': variables})
        if response.status_code==200:
            raw_response = json.loads(response.text)

            info = {
                'coverImage': raw_response['data']['Media']['coverImage']['extraLarge'],
                'title': raw_response['data']['Media']['title']['romaji'] ,
                'format': raw_response['data']['Media']['format'],
                'status': raw_response['data']['Media']['status'],
                'episodes': raw_response['data']['Media']['episodes'],
                'genres': ['#{0}'.format(x).replace(' ','_').replace('-','_') for x in raw_response['data']['Media']['genres']],
                'tags' : ['#{0}'.format(x['name']) for x in raw_response['data']['Media']['tags'][:5]],
                'year' : raw_response['data']['Media']['startDate']['year'],
                'description': translate.traducir(str(re.sub('<.*?>', '', raw_response['data']['Media']['description']))) if raw_response['data']['Media']['description'] else '',
            }

            return info
        else :
            print('get',response.status_code)
            return False
    except Exception as e:
        print('get',e)
        return False
