from django.urls import re_path
from AppReport.views import *

urlpatterns = [
    # DAILY SALE 
    re_path(r'/all_outlet_dates/(?P<code>.+)/', GetAllOutletDateView, name='AllOutletDate'),
    re_path(r'/daily_sale_report/(?P<code>.+)/', DailySaleView, name='DailySale'),
    re_path(r'/daily_sale_report_detail/(?P<code>.+)/', DailySaleDetailView, name='DailySaleDetail'),
    re_path(r'/sales_report/(?P<start_date>.+)/(?P<end_date>.+)/', SalesReportView, name='SalesReport'),
    re_path(r'/profit_report/', ProfitReportView, name='ProfitReport'),

]
