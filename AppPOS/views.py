from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.status import *


@api_view(['GET'])
def AllProductView(request):
    product = Product.objects.all()
    array = []
    if len(product) > 0:
        for i in range(len(product)):
            product_dict = dict()
            product_dict['product_name'] = product[i].product_name
            product_dict['sku'] = product[i].sku
            product_dict['size'] = product[i].size
            product_dict['color'] = product[i].color
            array.append(product_dict)
        return Response(array)
    return Response(status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
def ProductDetailView(request, code):
    product = Product.objects.filter(sku=code)
    array = []
    if len(product) > 0:
        for i in range(len(product)):
            product_dict = dict()
            product_dict['product_name'] = product[i].product_name
            product_dict['sku'] = product[i].sku
            product_dict['cost_price'] = product[i].cost_price
            product_dict['selling_price'] = product[i].selling_price
            array.append(product_dict)
        return Response(array)
    return Response(status=HTTP_404_NOT_FOUND)




### TRANSACTION VIEW
class AddTransactionView(generics.ListCreateAPIView):
    queryset = TransactionItem.objects.all()
    serializer_class = TransactionItemSerializer
    pagination_class = None


### ADDITIONAL FEE VIEW
class AddAdditionalFeeView(generics.ListCreateAPIView):
    queryset = AdditionalFee.objects.all()
    serializer_class = AdditionalFeeSerializer
    pagination_class = None


class GetAdditionalFeeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdditionalFee.objects.all()
    serializer_class = AdditionalFeeSerializer
    pagination_class = None


### SALESMAN VIEW
class AddSalesmanView(generics.ListCreateAPIView):
    queryset = Salesman.objects.all()
    serializer_class = AddSalesmanSerializer
    pagination_class = None


class GetSalesmanView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Salesman.objects.all()
    serializer_class = AddSalesmanSerializer
    pagination_class = None
    
    
### TRANSACTION RETURN VIEW
class TransactionReturnView(generics.ListCreateAPIView):
    queryset = TransactionReturn.objects.all()
    serializer_class = TransactionReturnSerializer
    pagination_class = None


@api_view(['GET'])
def GetAllInvoicesView(request):
    cursor = connections['default'].cursor()
    query = "select 'Invoice#: ' || split_part(invoice_code, '-', 2) as invoice, invoice_code from tbl_transaction order by invoice_code"
    cursor.execute(query)
    invoices = DistinctFetchAll(cursor)
    return Response(invoices)

@api_view(['GET'])    
def GetInvoiceProductsView(request, code):
    cursor = connections['default'].cursor()
    query = "select pr.sku, product_name, color, size  from tbl_transaction_item tri INNER JOIN tbl_product pr on tri.sku = pr.sku where invoice_code_id = '"+ code +"'"
    cursor.execute(query)
    invoice_products = DistinctFetchAll(cursor)
    if len(invoice_products) > 0:
        return Response(invoice_products)
    return Response("NO RECORD FOUND")


@api_view(['GET'])
def GetProductDetailView(request, code, sku):
    cursor = connections['default'].cursor()
    query = "select sku, quantity, rate, gross_total,per_discount, discounted_value, item_total from tbl_transaction_item where sku = '"+ sku +"' and invoice_code_id = '"+ code +"'"
    cursor.execute(query)
    invoice_products = DistinctFetchAll(cursor)
    array = []
    if len(invoice_products) > 0:
        # return_dict = dict()
          for x in range(len(invoice_products)):
            return_dict = dict()
            return_dict["sku"] = invoice_products[x]["sku"]
            return_dict["quantity"] = int(invoice_products[x]["quantity"])
            rate = int(invoice_products[x]["rate"]) - int((int(invoice_products[x]["rate"]) /100) * int(invoice_products[x]["per_discount"]))
            return_dict["rate"] = rate
            return_dict["gross_total"] = int(invoice_products[x]["gross_total"])
            return_dict["per_discount"] = int(invoice_products[x]["per_discount"])
            return_dict["discounted_value"] = int(invoice_products[x]["discounted_value"])
            return_dict["item_total"] = int(invoice_products[x]["item_total"])
            array.append(return_dict)
            return Response(array)
    return Response("NO RECORD FOUND")
    
    
    
    

    
    
