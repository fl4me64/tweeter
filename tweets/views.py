from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import TweetForm
from .models import Tweet

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if (request.headers.get('x-requested-with') == 'XMLHttpRequest'):
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if(request.headers.get('x-requested-with') == 'XMLHttpRequest'):
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and url_has_allowed_host_and_scheme(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if(request.headers.get('x-requested-with') == 'XMLHttpRequest'):
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})

def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "response": tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view(request, tweet_id, *args, **kwargs):
    data = {
        "id": tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
    
    return JsonResponse(data, status=status)
