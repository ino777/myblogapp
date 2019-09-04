""" Main app(blogs) admin settings """
from django.contrib import admin


from .models import Post, PostEval


class PostAdmin(admin.ModelAdmin):
    """ ModelAdmin for post """
    fieldsets = [
        (None, {'fields': ['id', 'title', 'text']}),
        ('Author', {'fields': ['author']}),
        ('Media', {'fields': ['image']}),
        ('Date information', {'fields': ['created_date', 'published_date']}),
    ]
    readonly_fields = ['id']
    list_display = ('title', 'author', 'created_date', 'published_date')
    list_filter = ['author', 'published_date']
    search_fields = ['title']

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(PostEval)
