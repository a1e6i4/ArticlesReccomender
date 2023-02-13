from django.contrib import admin
from articles.models import *

admin.site.register(Article)
admin.site.register(Like)
