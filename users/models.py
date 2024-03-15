from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=12, blank=True)
    ref_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')
    expiration_date = models.DateTimeField(null=True, blank=True)

    def is_ref_code_valid(self):
        return self.expiration_date is None or self.expiration_date > timezone.now()

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(pre_save, sender=Profile)
def delete_expired_ref_code(sender, instance, **kwargs):
    if instance.expiration_date and instance.expiration_date < timezone.now():
        instance.ref_code = ''
        instance.expiration_date = None
        Profile.objects.filter(pk=instance.pk).update(ref_code='', expiration_date=None)
