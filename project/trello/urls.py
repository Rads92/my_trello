from django.conf.urls import url
from django.contrib import admin
from trello.views import *
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'trello'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', BaseView.as_view(), name="base"),
    url(r'^login$', LoginView.as_view(), name="login"),
    url(r'^signup$', SignupView.as_view(), name="signup"),
    url(r'^logout$', logout_view, name="logout"),

    url(r'^create_list$', ListCreate.as_view(), name="create_list"),
    url(r'^copy_list/(?P<pk>[0-9]+)$', ListCopy.as_view(), name="copy_list"),
    url(r'^delete_list/(?P<pk>[0-9]+)$', ListDelete.as_view(), name="delete_list"),
    url(r'^delete_allcards/(?P<pk>[0-9]+)$', DeleteAllCards.as_view(), name="delete_lists_cards"),


    url(r'^create_card$', CardCreate.as_view(), name="create_card"),
    url(r'^edit_card/(?P<pk>[0-9]+)$', CardEdit.as_view(), name="edit_card"),
    url(r'^delete_card/(?P<pk>[0-9]+)$', CardDelete.as_view(), name="delete_card"),

    url(r'^detail_card/(?P<pk>[0-9]+)$', CardDetail.as_view(), name="detail_card"),

]

urlpatterns = format_suffix_patterns(urlpatterns)
