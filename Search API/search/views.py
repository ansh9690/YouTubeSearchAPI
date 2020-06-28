import requests
from django.shortcuts import render
from django.conf import settings
from isodate import parse_duration


# Create your views here.
def index(request):
    videos = []
    if request.method == 'POST':
        search_url = "https://www.googleapis.com/youtube/v3/search"
        video_url = "https://www.googleapis.com/youtube/v3/videos"
        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'type': 'video',
            'maxResults': 9,
            'channelId': 'UCdGQeihs84hyCssI2KuAPmA'
        }
        videos_ids = []
        r = requests.get(search_url, params=search_params)
        print(r)
        results = r.json()['items']
        for result in results:
            videos_ids.append(result['id']['videoId'])

        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet,contentDetails',
            'id': ','.join(videos_ids),
            'maxResults': 9
        }

        p = requests.get(video_url, params=video_params)
        results1 = p.json()['items']

        for result in results1:
            video_data = {
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={ result["id"] }',
                'title': result['snippet']['title'],
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'thumbnails': result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)
    else:
        channel_url = "https://www.googleapis.com/youtube/v3/channels"
        playlist_url = "https://www.googleapis.com/youtube/v3/playlistItems"
        videos_url = "https://www.googleapis.com/youtube/v3/videos"

        videos_list = []
        channel_params = {
            'part': 'contentDetails',
            'id': 'UCdGQeihs84hyCssI2KuAPmA',
            'key': settings.YOUTUBE_DATA_API_KEY,
        }
        r = requests.get(channel_url, params=channel_params)
        results = r.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        playlist_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet',
            'playlistId': results,
            'maxResults': 5,
        }
        p = requests.get(playlist_url, params=playlist_params)
        results1 = p.json()['items']

        for result in results1:
            print(results)
            videos_list.append(result['snippet']['resourceId']['videoId'])

        videos_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet',
            'id': ','.join(videos_list)
        }

        v = requests.get(videos_url, params=videos_params)
        results2 = v.json()['items']
        videos = []
        for res in results2:
            video_data = {
                'id': res['id'],
                'title': res['snippet']['title'],
            }

            videos.append(video_data)
        print(videos)
    context = {
        'videos': videos,
    }
    return render(request, 'search/index.html', context)
