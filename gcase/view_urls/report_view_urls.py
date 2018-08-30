from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from gcase.views import BacklogReportView, LanguageReportView, IndividualReportView,IndividualDetailReportView,ComponentReportView,\
                        PartnerReportMonthlyView,PartnerReportDetailView,PartnerNonPartnerReportView,ReviewRequestQualityReportView,\
                        DaReportView,PartnerReportTotalView,YearlyReportView

urlpatterns = [
    url(r'^report/backlog$', BacklogReportView.as_view(), name="backlog_report"),
    url(r'^report/language$', LanguageReportView.as_view(), name="language_report"),
    url(r'^report/individual$', IndividualReportView.as_view(), name="individual_report"),
    url(r'^report/individual_by_member$', IndividualDetailReportView.as_view(), name="individual_by_member_report"),
    url(r'^report/individual_details$', IndividualDetailReportView.as_view(), name="individual_detail_report"),
    url(r'^report/partner_monthly$', PartnerReportMonthlyView.as_view(), name="partner_report_monthly"),
    url(r'^report/partner_total$', PartnerReportTotalView.as_view(), name="partner_report_total"),
    url(r'^report/partner/details$', PartnerReportDetailView.as_view(), name="partner_report_detail"),
    url(r'^report/partner_nonpartner/$', PartnerNonPartnerReportView.as_view(), name="partner_nonpartner_report"),
    url(r'^report/review_request/quality$', ReviewRequestQualityReportView.as_view(), name="review_request_quality_report"),
    url(r'^report/component/$', ComponentReportView.as_view(), name="component_report_view"),
    url(r'^report/da_report/$', DaReportView.as_view(), name="da_report_view"),
    url(r'^yearly_report/$', YearlyReportView.as_view(), name="yearly_view")
]
