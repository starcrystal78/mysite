from django.db import models

# Create your models here.
class Subscribers(models.Model):
    email = models.CharField(max_length=100, blank=False, null=False, help_text="Your email")
    full_name = models.CharField(max_length=120, blank=False, null=False, help_text="full Name Please")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'
