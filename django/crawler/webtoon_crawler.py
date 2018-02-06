import os
import re
import requests
from bs4 import BeautifulSoup

# dir of project container
PATH_MODULE = os.path.abspath(__file__)
ROOT_DIR = os.path.dirname(PATH_MODULE)


class EpisodeData:
    """
    data for an episode
    """

    def __init__(self, episode_id, url_thumbnail, title, rating, created_date):
        self.episode_id = episode_id
        self.url_thumbnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date


def get_episode_list(webtoon_id, page):
    """
    webtoon list for a specific page with webtoons with own ID (from URL)
    :param webtoon_id:
    :param page:
    :return: list of webtoon
    """
    url = 'http://comic.naver.com/webtoon/list.nhn'
    params = {
        'titleId': webtoon_id,
        'page': page,
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

    result = []
    for tr in tr_list:
        # in case there's tr.band_banner, ignore it - banner treatment way(2)
        # try later
        episode_id_container = tr.select_one('td.title > a ').get('href')
        episode_id = re.search('no=(\d+)', episode_id_container).group(1)
        url_thumbnail = tr.select_one('td:nth-of-type(1) > a > img').get('src')
        title = tr.select_one('td.title > a').text
        rating = tr.select_one('td:nth-of-type(3) > div.rating_type > strong').text
        created_date = tr.select_one('td.num').text

        episode = EpisodeData(
            episode_id=episode_id,
            url_thumbnail=url_thumbnail,
            title=title,
            rating=rating,
            created_date=created_date
        )
        result.append(episode)
    # a list of EpisodeData instances
    return result


if __name__ == '__main__':
    episode_list = get_episode_list(698918, 1)
    for row in episode_list:
        print(f'{row.url_thumbnail}\n'
              f'{row.episode_id} th episode   | title:{row.title}   '
              f'| rating:{row.rating}   | created_date:{row.created_date}\n')
