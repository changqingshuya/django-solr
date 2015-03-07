from django.db import models
class TorrentInfo(models.Model):
    name = models.TextField()
    creation_date = models.DateField()
    file_list = models.TextField()
    files = models.TextField()
    tracker_url = models.TextField()
    client_name = models.TextField()
    hashInfo = models.TextField()
    hotCount = models.IntegerField()
    clickCount = models.IntegerField()
    current_date = models.DateField()