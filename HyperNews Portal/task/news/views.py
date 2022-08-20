import itertools
import json
import random

from django.http import HttpResponse, Http404
from django.views import View
from django.conf import settings
from django.shortcuts import render, redirect
from datetime import datetime


def soon(request):
    return redirect('/news/')


def read_json():
    with open(settings.NEWS_JSON_PATH, 'r') as json_file:
        content = json.load(json_file)
    return content


class NewsView(View):
    def get(self, request, news_id):
        news = read_json()
        item = next((item for item in news if item['link'] == int(news_id)), None)
        if item is None:
            raise Http404
        return render(request, "index.html", context=item)


class MainView(View):
    def get(self, request):
        news = read_json()
        sorted_news = sorted(news, key=lambda i: i['created'], reverse=True)
        groupped_news = itertools.groupby(sorted_news, lambda i: i['created'][:10])
        jedd = {}
        q = ''
        if 'q' in request.GET.keys():
            q = request.GET['q']
        for news_date, day_news in groupped_news:
            day_list = [news_dict for news_dict in day_news if q == '' or q in news_dict['title']]
            if len(day_list) > 0:
                jedd[news_date] = day_list
        context = {"title": 'Hyper news', "groupped_news": jedd}
        return render(request, "main.html", context=context)


class CreateView(View):
    def get(self, request):
        return render(request, "create.html")

    def post(self, request):
        title = request.POST.get('title')
        text = request.POST.get('text')
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        num = random.randint(10, 1000000)
        news = read_json()
        news.append({
            "created": str(date),
            "text": text,
            "title": title,
            "link": str(num)})
        with open(settings.NEWS_JSON_PATH, 'w') as json_file:
            json.dump(news, json_file)
        return redirect('/news/')
