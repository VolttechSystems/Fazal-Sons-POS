from django.urls import re_path
from AppReport.views import *

urlpatterns = [
    # DAILY SALE 
    re_path(r'/all_outlet_dates/(?P<outlet>.+)/', GetAllOutletDateView, name='AllOutletDate'),                  ## GET ALL OUTLETS DATES IN TRANSACTION
    re_path(r'/daily_sale_report/(?P<outlet>.+)/(?P<date>.+)/', DailySaleView, name='DailySale'),               ## DAILY SALE REPORT OVERVIEW
    re_path(r'/daily_sale_report_detail/(?P<invoice_code>.+)/', DailySaleDetailView, name='DailySaleDetail'),   ## DAILY SALE REPORT DETAIL
    re_path(r'/sales_report/(?P<outlet>.+)/(?P<start_date>.+)/(?P<end_date>.+)/', SalesReportView, name='SalesReport'),        ## DAY WISE TOTAL REPORT
    re_path(r'/profit_report/(?P<outlet>.+)/(?P<date>.+)/', ProfitReportView, name='ProfitReport'),             ## PROFIT REPORT
    re_path(r'/outlet_wise_salesman/(?P<outlet>.+)/', OutletWiseSalesmanView, name='OutletWiseSalesman'),        ## GET SALESMAN ACCORDING TO OUTLET
    re_path(r'/salesman_commission_report/(?P<outlet>.+)/(?P<salesman>.+)/(?P<start_date>.+)/(?P<end_date>.+)/', SalesmanCommissionReportView, name='SalesmanCommissionReport'),    ## SALESMAN COMMISSION REPORT
]


