from django.contrib import admin
from quote.models import Record, Query


class RecordAdmin( admin.ModelAdmin ):
    list_display = ('name', 'telnum', 
        'price', 'fee', 'annotation')
        

# class RecordInline( admin.TabularInline ):
    # model = Query.queryRes.through
        
class QueryAdmin( admin.ModelAdmin ):
    list_display = ('user', 'queryStr', 'isRegistered', 'time')
    # inlines = [RecordInline]
    
    
# Register your models here.
admin.site.register(Record, RecordAdmin)
admin.site.register(Query, QueryAdmin)