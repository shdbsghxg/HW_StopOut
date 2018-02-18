from django.shortcuts import render
from .models import Webtoon


def webtoon_list(request):

    webtoons = Webtoon.objects.all()
    context = {
        'webtoons': webtoons,
    }
    return render(request, 'webtoon_list.html', context)


def webtoon_detail(request, pk):

    webtoon = Webtoon.objects.get(pk=pk)
    webtoon.get_episode_list()
    context = {
        'webtoon': webtoon,
    }
    return render(request, 'webtoon_detail.html', context)
