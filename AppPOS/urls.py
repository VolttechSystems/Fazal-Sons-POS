from django.urls import re_path
from .views import*


urlpatterns = [
        
        ### ADDITIONAL FEE URL
        re_path(r'add_additional_fee', AddAdditionalFeeView.as_view(), name='AddAdditionalFee'),
        re_path(r'action_additional_fee/(?P<pk>.+)/', GetAdditionalFeeView.as_view(), name='GetAdditionalFee'),
        ### SALESMAN URL
        re_path(r'add_salesman', AddSalesmanView.as_view(), name='AddSalesman'),
        re_path(r'action_salesman/(?P<pk>.+)/', GetSalesmanView.as_view(), name='GetSalesman'),
        ### TRANSACTION URL
        re_path(r'all_product', AllProductView, name='AllProduct'),
        re_path(r'products_detail/(?P<code>.+)/', ProductDetailView, name='ProductDetail'),
        re_path(r'add_transaction', AddTransactionView.as_view(), name='AddTransaction'),
        ### TRANSACTION RETURN URL
        re_path(r'transactions_return', TransactionReturnView.as_view(), name='TransactionReturn'),
        re_path(r'get_all_invoices/', GetAllInvoicesView, name='GetInvoices'),
        re_path(r'get_invoice_products/(?P<code>.+)/', GetInvoiceProductsView, name='GetInvoiceProduct'),
        re_path(r'get_product_detail/(?P<code>.+)/(?P<sku>.+)/', GetProductDetailView, name='GetProductDetail'),
]