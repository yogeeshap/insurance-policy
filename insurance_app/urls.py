
from django.conf.urls import url, include
from .views import PolicyDetailsListView,PolicyDetailsView,MonthWisePolicyView

app_name = 'insurance'
urlpatterns = [
    url(r'^policy/list/$',PolicyDetailsListView.as_view(),name='policy_list'),
    url(r'^policy/monthwise/list/$',MonthWisePolicyView.as_view(),name='month_wise_policy'),
    url(r'^policy/(?P<pk>[0-9]+)/$',PolicyDetailsView.as_view(),name='policy_update'),
]
