from django.db import models


class UserSiteModel(models.Model):
    site_name = models.CharField(max_length=45, verbose_name='site_name')
    site_path = models.URLField(max_length=200, verbose_name='site_path', unique=True)
    data_sent = models.PositiveIntegerField(verbose_name='data_sent', null=True, blank=True)
    data_loaded = models.PositiveIntegerField(verbose_name='data_loaded', null=True, blank=True)
    number_visits = models.PositiveIntegerField(verbose_name='data_loaded', null=True, blank=True)

    class Meta:
        verbose_name = "user_site"
        verbose_name_plural = "user_sites"

    def __str__(self):
        return self.site_name
