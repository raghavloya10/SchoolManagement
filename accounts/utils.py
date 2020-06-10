import string
import random
from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_email_slug_generator(instance,new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.user.email)

    mod = instance.__class__
    qs_exists = mod.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{}-{}".format(slug,random_string_generator(size=4))
        return unique_email_slug_generator(instance,new_slug)
    return slug

def unique_name_slug_generator(instance,new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    mod = instance.__class__
    qs_exists = mod.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{}-{}".format(slug,random_string_generator(size=4))
        return unique_name_slug_generator(instance,new_slug)
    return slug
