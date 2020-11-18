import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from line.models import line_user
# Create your views here.

def send_basic(token):
    msg = f"hello world"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers,
                    params=payload)

def auth(request):
    url = 'https://notify-bot.line.me/oauth/authorize?'
    response_type = 'code'
    client_id = settings.LINE_CLIENT_ID
    redirect_uri = 'http://127.0.0.1:8000/callback/'
    scope = 'notify'
    state = 'NO_STATE'
    url = f'{url}response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}'
    return redirect(url)


def callback(request):
    token = request.GET['code']
    url = 'https://notify-bot.line.me/oauth/token'
    payload = {'grant_type': 'authorization_code', 
            'code': token,
            'redirect_uri': 'http://127.0.0.1:8000/callback/',
            'client_id': settings.LINE_CLIENT_ID,
            'client_secret': settings.LINE_CLIENT_SECRET
    }
    r = requests.post(url, params = payload)
    if(r.ok):
        token = r.json()['access_token']
        (target_type, target) = get_status(token)
        unit = line_user.objects.create(token=token, target_type=target_type, target=target) 
        unit.save()
        send_basic(token)
        return HttpResponse("Sent!")
    else:
        return HttpResponse("Fail")


def get_status(token):
    url = 'https://notify-api.line.me/api/status'
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.get(url, headers=headers)
    if(r.ok):
        target_type = r.json()['targetType']
        target = r.json()['target']
        return target_type, target
    else:
        return 'fail'