from django.conf.urls import url
from django.contrib import admin
from trello.views import *

app_name = 'trello'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', BaseView.as_view(), name="base"),
    url(r'^create_list$', ListCreate.as_view(), name="create_list"),
    url(r'^create_card$', CardCreate.as_view(), name="create_card"),

]
