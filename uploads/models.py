from django.db import models
from subjects.models import Subject
from .validators import validate_file_extension

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

    def __str__(self):
        return self.title

    def delete(self,*args,**kwargs):
        self.pdf.delete()
        super().delete(*args,**kwargs)
