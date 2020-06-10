from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save, pre_save
from accounts.utils import unique_email_slug_generator
from accounts.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    broadcast = models.BooleanField(default=False)
    slug = models.SlugField(max_length=210,blank=True,null=True,editable=False)

    @property
    def get_html_url(self):
        url = reverse('students:event_edit', args=(self.id,))
        return f"<a href={url}> {self.title} </a>"

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_email_slug_generator(instance)

pre_save.connect(slug_generator,sender=Event)
