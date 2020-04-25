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
            'maxResults': 9
        }
        videos_ids = []
        r = requests.get(search_url, params=search_params)
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
    context = {
        'videos': videos,
    }
    return render(request, 'search/index.html', context)
