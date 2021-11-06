from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from PIL import Image

# Create your models here.
class Profile(models.Model):
    roles = (
        ("Operator", "Operator"),
        ("Supervisor", "Supervisor"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=roles)
    service_number = models.CharField(max_length=12, default="00000000")
    bio = models.TextField(default="No bio set")
    image = models.ImageField(default="default_profile_pic.jpg", upload_to="profile_pics")
    staff = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    # DATA COLLECTION
    ip_address = models.CharField(default='Unknown', max_length=100, null=True, blank=True)
    isp = models.CharField(default='Unknown', max_length=100, null=True, blank=True)
    provider = models.CharField(default='Unknown', max_length=200, null=True, blank=True)
    region = models.CharField(default='Unknown', max_length=100, null=True, blank=True)
    country = models.CharField(default='Unknown', max_length=100, null=True, blank=True)
    city = models.CharField(default='Unknown', max_length=100, null=True, blank=True)
    latitude = models.CharField(default='Unknown', max_length=100, null=True, blank=True)
    longitude = models.CharField(default='Unknown', max_length=100, null=True, blank=True)
    os = models.CharField(default='Unknown', max_length=100, null=True, blank=True)
    client = models.CharField(default='Unknown', max_length=100, null=True, blank=True)
    device = models.CharField(default='Unknown', max_length=100, null=True, blank=True)


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = ['username', 'get_service_number', 'email', 'get_role', 'get_approved_status', 'get_staff_status']

    def get_approved_status(self, obj):
        return obj.profile.approved
    get_approved_status.admin_order_field = 'approved'
    get_approved_status.short_description = 'Approved status'

    def get_staff_status(self, obj):
        return obj.profile.staff
    get_staff_status.admin_order_field = 'staff'
    get_staff_status.short_description = 'staff status'

    def get_role(self, obj):
        return obj.profile.role
    get_role.admin_order_field = 'role'
    get_role.short_description = 'Role'

    def get_service_number(self, obj):
        return obj.profile.service_number
    get_service_number.admin_order_field = 'service_number'
    get_service_number.short_description = 'Service Number'



    
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.Profile.save()
