from django.db import models


class Webtoon(models.Model):
    # webtoon_id
    # title
    pass

class Episode(models.Model):
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE)
    # episode_id
    # title
    # rating
    # created_date
    pass

