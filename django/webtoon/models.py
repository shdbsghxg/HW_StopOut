import re
import requests
from bs4 import BeautifulSoup
from django.db import models


class Webtoon(models.Model):
    webtoon_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)

    def __str__(self):
        return '{id}   |   {title}'.format(
            id=self.webtoon_id,
            title=self.title,
        )

    def get_episode_list(self):

        url = 'http://comic.naver.com/webtoon/list.nhn'
        params = {
            'titleId': self.webtoon_id,
            'page': 1,
        }

        response = requests.get(url, params)
        soup = BeautifulSoup(response.text, 'lxml')
        tr_list = soup.select('table.viewList > tr')

        # in case there's tr.band_banner, removing it - banner treatment way(1)
        tr_banner = soup.select('tr.band_banner')

        # note) soup(lxml).select() --> a list
        for row in tr_banner:
            if row in tr_list:
                del tr_list[tr_list.index(row)]

        for tr in tr_list:
            # in case there's tr.band_banner, ignore it - banner treatment way(2)
            # try later
            episode_id_container = tr.select_one('td.title > a ').get('href')
            episode_id = re.search('no=(\d+)', episode_id_container).group(1)
            # url_thumbnail = tr.select_one('td:nth-of-type(1) > a > img').get('src')
            title = tr.select_one('td.title > a').text
            rating = tr.select_one('td:nth-of-type(3) > div.rating_type > strong').text
            created_date = tr.select_one('td.num').text

            if not self.episode_set.all().filter(episode_id=episode_id).exists():
                episode = self.episode_set.create(
                    episode_id=episode_id,
                    # url_thumbnail=url_thumbnail,
                    title=title,
                    rating=rating,
                    created_date=created_date,
                )


class Episode(models.Model):
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE)
    episode_id = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    rating = models.CharField(max_length=10)
    created_date = models.CharField(max_length=100)

    def __str__(self):
        return '{title}  |  {rating}  |  {date}'.format(
            episode_id=self.episode_id,
            title=self.title,
            rating=self.rating,
            date=self.created_date,
        )