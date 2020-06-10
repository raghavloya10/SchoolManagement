from django.db import models
from django.contrib.auth.models import (
        AbstractBaseUser, BaseUserManager
)
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name="", last_name=""):
        if not email:
            raise ValueError('User must have an email')
        if not password:
            raise ValueError('User must have a password')
        user_obj = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name
         )
        user_obj.set_password(password)
        user_obj.staff = False
        user_obj.admin = False
        user_obj.active = True
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password = password
        )
        user.staff = True
        return user

    def create_superuser(self, email,password=None):
        user = self.create_user(
            email,
            password = password
        )
        user.active = True
        user.admin =True
        user.staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
        default='s@gmail.com'
    )
    contact_no = models.CharField(max_length=10,blank=True)
    first_name = models.CharField(max_length=200,default='s')
    last_name = models.CharField(max_length=200,default='0')
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    address = models.CharField(max_length=200,default="",blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    date_of_birth = models.DateField(
        auto_now_add=False,
        help_text = 'Format: YYYY-MM-DD',
        blank=True,
        null=True
        )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

    @property
    def is_staff(self):
        if self.admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
