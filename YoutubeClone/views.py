from django.shortcuts import render
from Videos.models import Video
from allauth.socialaccount.models import SocialAccount
from googleapiclient.discovery import build
from datetime import datetime,timezone

def home(request):
    cats = ['All', 'CSS','Music' ,'News','Comedy','Live','Gaming','Mixes','Computers','Tech','Trending','Recently Uploaded','Watched','New to you']
    API_KEY = 'AIzaSyBudKc1kMuS8gXUN1BFxZNsZN-oPQC-kYs'
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    region_code = 'US' 
    x = youtube.videos().list(
        part='snippet,statistics',
        chart='mostPopular',
        regionCode=region_code,
        videoCategoryId='0',
        maxResults=9
    )
    response = x.execute()
    videos = []
    for video_item in response['items']:
        video_id = video_item['id']
        channel_request = youtube.channels().list(
            part='snippet',
            id=video_item['snippet']['channelId']
        )
        channel_response = channel_request.execute()
        channel_info = {
            'title': channel_response['items'][0]['snippet']['title'],
            'thumbnail_url': channel_response['items'][0]['snippet']['thumbnails']['default']['url'],
        }
        published_at_str = video_item['snippet']['publishedAt']

        published_at = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%S%z")
        current_time = datetime.now(timezone.utc)
        time_difference = current_time - published_at
        seconds = time_difference.seconds
        if seconds<60:
            ans = str(seconds) + " seconds ago"
        elif seconds<3600:
            ans=  str(seconds//60) + " minutes ago"
        elif seconds < 3600*24:
            ans = str(seconds//3600) + " hours ago"
        else:
            days = time_difference.days
            if days <30:
                ans = str(days) + " days ago"
            elif days<365:
                ans = str(days//30) + " months ago"
            else:
                ans = str(days//365) + " years ago"
        v= int(video_item['statistics']['viewCount'])
        if (v<1000):
            ans2 = str(v) + ' views'
        elif (v<1000*1000):
            ans2= str(v//1000)+ "K views"
        else:
            ans2= str(v//(1000*1000)) + "M views"
        if request.user.is_authenticated:
            social_account = SocialAccount.objects.get(user=request.user, provider='google')
            extra_data = social_account.extra_data
        else:
            extra_data=None
        video_info = {
            'title': video_item['snippet']['title'],
            'videoId': video_id,
            'thumbnail_url': video_item['snippet']['thumbnails']['standard']['url'],
            'channel_info': channel_info,
            'view_count': ans2,
            'years_difference':ans
        }
        videos.append(video_info)
    return render(request,'home.html',{'cats':cats,'extra_data':extra_data,'videos': videos})

def watch(request,video_id):
    API_KEY = 'AIzaSyBudKc1kMuS8gXUN1BFxZNsZN-oPQC-kYs'
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    x = youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    )
    response = x.execute()

    channel_request = youtube.channels().list(
        part='snippet,statistics',
        id=response['items'][0]['snippet']['channelId']
    )
    channel_response = channel_request.execute()
    channel_info = {
            'title': channel_response['items'][0]['snippet']['title'],
            'thumbnail_url': channel_response['items'][0]['snippet']['thumbnails']['default']['url'],
            
    }
    published_at_str = response['items'][0]['snippet']['publishedAt']

    published_at = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%S%z")
    current_time = datetime.now(timezone.utc)
    time_difference = current_time - published_at
    seconds = time_difference.seconds
    if seconds<60:
        ans = str(seconds) + " seconds ago"
    elif seconds<3600:
        ans=  str(seconds//60) + " minutes ago"
    elif seconds < 3600*24:
        ans = str(seconds//3600) + " hours ago"
    else:
        days = time_difference.days
        if days <30:
            ans = str(days) + " days ago"
        elif days<365:
            ans = str(days//30) + " months ago"
        else:
            ans = str(days//365) + " years ago"
    v= int(response['items'][0]['statistics']['viewCount'])
    
    if (v<1000):
        ans2 = str(v) + ' views'
    elif (v<1000*1000):
        ans2= str(v//1000)+ "K views"
    else:
        ans2= str(v//(1000*1000)) + "M views"
    w=int(channel_response['items'][0]['statistics']['subscriberCount'])
    if (w<1000):
        qw = str(w) + ' subscribers'
    elif (w<1000*1000):
        qw= str(w//1000)+ "K subscribers"
    else:
        qw= str(w//(1000*1000)) + "M subscribers"
    comments_request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText'
    )
    comments_response = comments_request.execute()

    comments = [comment['snippet']['topLevelComment']['snippet']['textDisplay'] for comment in comments_response['items']]


    vid = {
            'title': response['items'][0]['snippet']['title'],
            'channel_info': channel_info,
            'view_count': ans2,
            'years_difference':ans,
            'subs':qw
        }
    if request.user.is_authenticated:
        social_account = SocialAccount.objects.get(user=request.user, provider='google')
        extra_data = social_account.extra_data
    else:
        extra_data=None
    for comment in comments:
        print(comment)
    return render(request,'watch.html',{'id':video_id,'vid':vid,'extra_data':extra_data,'comments':comments})