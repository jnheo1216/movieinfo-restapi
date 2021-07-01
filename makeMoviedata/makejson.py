import requests 
import json

print('helloworld')
file_path = "./moviesFinal.json"
jjssoonn = []

for i in range(1, 8):
    URL = f'https://api.themoviedb.org/3/movie/popular?api_key=b4893f302d08c4a823cdf51e8fcee9cc&language=ko-KR&page={i}' 
    response = requests.get(URL)
    # print(response.status_code)
    jjssoonn += response.json()['results']

# print(type(jjssoonn))
# print(jjssoonn)

export_json = []
pk_num = 1
for i in range(len(jjssoonn)):
    idVal = jjssoonn[i]['id']
    URL = f"https://api.themoviedb.org/3/movie/{idVal}/videos?api_key=b4893f302d08c4a823cdf51e8fcee9cc&language=ko-KR"
    response = requests.get(URL)
    # print(response.json()['results'])
    video_result = response.json()['results']

    if video_result == [] or jjssoonn[i]['backdrop_path']=='':
        pass
    else:
        print(video_result[0]['key'])
        tmp = {}
        tmp['model'] =  "movies.movie"
        tmp['pk'] =  pk_num
        pk_num += 1

        tmp_fields = {
            'poster_path': jjssoonn[i]['poster_path'],
            'title': jjssoonn[i]['title'],
            'popularity': jjssoonn[i]['popularity'],
            'vote_count': jjssoonn[i]['vote_count'],
            'vote_average': jjssoonn[i]['vote_average'],
            'overview': jjssoonn[i]['overview'],
            'movie_id': jjssoonn[i]['id'],
            'backdrop_path': jjssoonn[i]['backdrop_path'],
            'key': video_result[0]['key'],
        }
        try:
            tmp_fields['release_date'] = jjssoonn[i]['release_date']
        except:
            tmp_fields['release_date'] = "1900-01-01"
        tmp['fields'] = tmp_fields
        export_json.append(tmp)

with open(file_path, 'w', encoding='UTF-8') as file:
     file.write(json.dumps(export_json, ensure_ascii=False, indent=4))
