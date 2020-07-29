from django.db import models
from subjects.models import Subject
from .validators import validate_file_extension
from accounts.utils import unique_email_slug_generator
from django.db.models.signals import pre_save

TYPE_CHOICES = (
    ("Assignment","Assignment"),
    ("Notice","Notice"),
    ("Announcement","Announcement"),
    ("Reference","Reference"),
    ("Marksheet","Marksheet")
)

class Upload(models.Model):
    title = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    type = models.CharField(max_length=20,
                           choices=TYPE_CHOICES,
                           default="Assignment")
    pdf = models.FileField(upload_to="uploads/",
                           validators=[validate_file_extension])
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=210,blank=True,null=True, editable=False)

    def __str__(self):
        return self.title

    def delete(self,*args,**kwargs):
        self.pdf.delete()
        super().delete(*args,**kwargs)

import string
import random
from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance,new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    mod = instance.__class__
    qs_exists = mod.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{}-{}".format(slug,random_string_generator(size=4))
        return unique_slug_generator(instance,new_slug)
    return slug

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator,sender=Upload)