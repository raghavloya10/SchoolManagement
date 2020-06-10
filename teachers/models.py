from django.db import models
from accounts.models import User
from accounts.utils import unique_email_slug_generator
from django.db.models.signals import pre_save

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    is_class_teacher = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add =True)
    slug = models.SlugField(max_length=210,blank=True,null=True, editable=False)

    class Meta:
        default_related_name = 'teachers'

    def __str__(self):
        return self.user.get_full_name()

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_email_slug_generator(instance)

pre_save.connect(slug_generator,sender=Teacher)


# from django.db.models.signals import post_save
# from django.dispatch import receiver

# @receiver(post_save, sender=auth_User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Teacher.objects.create(user=instance)
#
# @receiver(post_save, sender=auth_User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
