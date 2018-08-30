from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from gcase.views import ReviewRequestListView, ReviewRequestCsv2DbView,ReviewRequestAddView,ReviewRequestUpdateView

urlpatterns = [
    url(r'^review_request/$', ReviewRequestListView.as_view(), name="review_request_list"),
    url(r'^review_request/add$', ReviewRequestAddView.as_view(), name="review_request_add"),
    url(r'^review_request/edit$', ReviewRequestUpdateView.as_view(), name="review_request_edit"),
    url(r'^request_csv_2db/insert$', ReviewRequestCsv2DbView.as_view(), name="request_csv2_db"),

]
