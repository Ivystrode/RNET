from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin
from datetime import datetime
from PIL import Image
import random
import uuid
from stdimage import StdImageField


# ==========MODEL FUNCTIONS==========

def unit_folder(instance, filename):
    """
    I think this is redundant now
    """
    print("UNIT DIRECTORY FUNCTION")

    base_filename, file_extension = os.path.splitext(filename)
    dt = datetime.now().strftime("%Y%m%d%H%M")
    nums = '1234567890'
    randomid = ''.join((random.choice(nums)) for x in range(3))

    print("datetime string: " + str(dt))
    print("random id: " + str(randomid))

    new_filename = f'{randomid}{dt}'
    parent_unit = Unit.objects.get(title=instance.unit.name)
    print(str(parent_unit))
    unit_name = parent_unit.slug
    print("saving:")
    print(new_filename)
    print("to")
    print(unit_name)
    return '/'.join(['units/', unit_name, new_filename + file_extension])
    
# ==========MODELS==========

class Unit(models.Model):
    id = models.TextField(db_column='id', blank=True, primary_key=True)  
    name = models.TextField(db_column='Name', blank=True, null=True)  
    address = models.TextField(db_column='Address', blank=True, null=True) 
    type = models.TextField(db_column='Type', blank=True, null=True)
    status = models.TextField(db_column='Status', blank=True, null=True)
    last_statrep = models.TextField(blank=True, null=True)
    location = models.TextField(default="51.183862090545, -4.669410763157165", blank=True, null=True)
    # slug = models.SlugField()

    class Meta:
        managed = False
        db_table = 'units'
        
    def __str__(self):
        return str(self.name)# + ": " + str(self.type)
        
class UnitPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='photos')

    # thumb = models.ImageField(upload_to=thumb_folder)

    photo = StdImageField(upload_to=unit_folder, variations = {'thumbnail': {'width': 300, 'height': 300, 'crop':False}})
    # stdimage allows standardized file renaming and thumbnail creation
    # figure out how to use the thumbnail...
    # can replace the thumb = models.imagefield above this block

    caption = models.CharField(max_length=100)
    time = models.DateTimeField(default=timezone.localtime(timezone.now()))

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return str(self.id) + ": " + str(self.caption)
    
class UnitObjectDetection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='object_detections')
    time = models.DateTimeField(default=timezone.localtime(timezone.now()))
    object_detected = models.CharField(default='Unknown', max_length=200, null=True, blank=True)
    
    class Meta:
        ordering = ['-time']

    def __str__(self):
        return str(self.object_detected) + ": " + str(self.time)
    
    
# ==========MODEL ADMIN==========

class UnitPhotoInline(admin.TabularInline):
    model = UnitPhoto
class UnitAdmin(admin.ModelAdmin):
    search_fields = ['name', 'type']
    list_display = ['name', 'type']
    inlines = [UnitPhotoInline]
