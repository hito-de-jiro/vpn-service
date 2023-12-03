from django.db import models


class UserSiteModel(models.Model):
    site_name = models.SlugField(max_length=45, verbose_name='site_name')
    site_path = models.URLField(max_length=200, verbose_name='site_path', unique=True)

    class Meta:
        verbose_name = "user_site"
        verbose_name_plural = "user_sites"

    def __str__(self):
        return self.site_name


class SiteInfoModel(models.Model):
    data_sent = models.FloatField(verbose_name='data_sent', null=True, blank=True)
    data_loaded = models.FloatField(verbose_name='data_loaded', null=True, blank=True)
    number_visits = models.PositiveIntegerField(verbose_name='number_visits', default=0, null=True, blank=True)
    user_site = models.ForeignKey(UserSiteModel, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "site_info"
        verbose_name_plural = "site_info"

