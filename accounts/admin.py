from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
#
# class UserChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     password hash display field.
#     """
#     password = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = User
#         fields = ('email', 'password','date_of_birth','first_name','last_name','active', 'admin','is_student','is_teacher')
#         # to be changed
#
#     def clean_password(self):
#         # Regardless of what the user provides, return the initial value.
#         # This is done here, rather than on the field, because the
#         # field does not have access to the initial value
#         return self.initial["password"]
#
# class UserAdmin(BaseUserAdmin):
#     form = UserChangeForm
#     add_form = UserSignupForm
#     list_display = ('email', 'first_name','last_name','date_of_birth')
#     list_filter = ('admin','is_teacher','is_student')
#     fieldsets = (
#         (None, {'fields': ('first_name','last_name','email', 'password')}),
#         ('Personal info', {'fields': ('date_of_birth','profile_pic')}),
#         ('Role', {'fields': ('is_teacher','is_student')}),
#         ('Permissions', {'fields': ('admin',)}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'date_of_birth', 'password1', 'password2')}
#         ),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ()

admin.site.register(User)
admin.site.unregister(Group)
