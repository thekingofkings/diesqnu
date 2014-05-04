from django.contrib import admin
from quote.models import Record


class RecordAdmin( admin.ModelAdmin ):
    list_display = ('name', 'telnum', 
        'price', 'fee', 'annotation')
    
    
# Register your models here.
admin.site.register(Record, RecordAdmin)