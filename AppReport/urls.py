from django.urls import re_path
from AppReport.views import *

urlpatterns = [
    # DAILY SALE 
    re_path(r'/all_outlet_dates/(?P<outlet_code>.+)/', GetAllOutletDateView, name='AllOutletDate'),
    re_path(r'/daily_sale_report/(?P<outlet_code>.+)/(?P<date>.+)/', DailySaleView, name='DailySale'),
    re_path(r'/daily_sale_report_detail/(?P<invoice_code>.+)/', DailySaleDetailView, name='DailySaleDetail'),
    re_path(r'/sales_report/(?P<start_date>.+)/(?P<end_date>.+)/', SalesReportView, name='SalesReport'),
    # re_path(r'/profit_report/', ProfitReportView, name='ProfitReport'),
    re_path(r'/profit_report/(?P<outlet_code>.+)/(?P<date>.+)/', ProfitReportView, name='ProfitReport'),

]


# Salesman Commission Report
# transaction - return transaction report
# Get ALL Customer API


# select tr_item.created_at::date, invoice_code, tr_item.sku, pr.product_name, tr_item.quantity, pr.selling_price  , pr.selling_price::INTEGER * tr_item.quantity::INTEGER as total   from tbl_transaction tr 
# INNER JOIN tbl_transaction_item tr_item on tr.invoice_code = tr_item.invoice_code_id
# INNER JOIN tbl_product pr on tr_item.sku = pr.sku
# INNER JOIN tbl_salesman sl on tr.salesman_code_id = sl.salesman_code