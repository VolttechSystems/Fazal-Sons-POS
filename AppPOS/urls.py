from django.urls import re_path
from .views import*

urlpatterns = [
        ### ADDITIONAL FEE URL
        re_path(r'add_additional_fee', AddAdditionalFeeView.as_view(), name='AddAdditionalFee'),
        re_path(r'action_additional_fee/(?P<pk>.+)/', GetAdditionalFeeView.as_view(), name='GetAdditionalFee'),
        ### SALESMAN URL
        re_path(r'add_salesman', AddSalesmanView, name='AddSalesman'),
        re_path(r'action_salesman/(?P<pk>.+)/', GetSalesmanView.as_view(), name='GetSalesman'),
        re_path(r'outlet-wise-salesman/(?P<outlet_id>.+)/', GetOutletWiseSalesmanView, name='GetOutletWiseSalesmanView'),
        ### CUSTOMER URL IN POS
        re_path(r'add-customer-in-pos', AddCustomerInPOSView.as_view(), name='AddCustomer'),
        ### PAYMENT METHOD URL
        re_path(r'add_payment/(?P<shop>.+)/', AddPaymentView.as_view(), name='AddPayment'),
        re_path(r'action_payment/(?P<shop>.+)/(?P<pk>.+)/', GetPaymentView.as_view(), name='GetPayment'),
        ### TRANSACTION URL
        # re_path(r'all_product/(?P<outlet>.+)/', AllProductView, name='AllProduct'),
        re_path(r'all_product/(?P<outlet_id>.+)/', AllProductView, name='AllProduct'),
        re_path(r'products_detail/(?P<code>.+)/', ProductDetailView, name='ProductDetail'),
        re_path(r'add_transaction', AddTransactionView.as_view(), name='AddTransaction'),
        ### TRANSACTION RETURN URL
        re_path(r'get_all_invoices/(?P<outlet>.+)', GetAllInvoicesView, name='GetInvoices'),
        re_path(r'get_invoice_products/(?P<code>.+)/', GetInvoiceProductsView, name='GetInvoiceProduct'),
        re_path(r'get_product_detail/(?P<code>.+)/(?P<sku>.+)/', GetProductDetailView, name='GetProductDetail'),
         re_path(r'transactions_return', TransactionReturnView.as_view(), name='TransactionReturn'),
        ### DUE RECEIVABLE URL
        re_path(r'get_due_invoices/(?P<outlet>.+)', GetDueInvoicesView, name='GetDueInvoices'),
        re_path(r'get_amount_of_due_invoices/(?P<invoice_code>.+)', GetDueInvoiceAmountView, name='GetDueInvoiceAmount'),
        re_path(r'receive_due_invoice/(?P<invoice_code>.+)', ReceiveDueInvoiceView, name='ReceiveDueInvoice'),
         ### TODAY SALE REPORT
        re_path(r'today_sale_report/(?P<outlet_id>.+)', TodaySaleReportView, name='TodaySaleReport'),   
         
]


##### outlet wise product list in transaction
###### outlet wise salesman in transaction

