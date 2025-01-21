from .models import *
from .serializer import *
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.status import *
from .serializer import ProductSerializer
from datetime import date
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from AppProduct.models import *
from .permissions import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Value, FloatField
from django.db.models.functions import Cast

@api_view(['GET'])
def AllProductView(request, outlet_id):
    try:
        get_outlet = Outlet.objects.get(id=outlet_id)
    except Outlet.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    product = Product.objects.filter(outlet_id=outlet_id)
    array = []
    if product.exists():
        for i in range(len(product)):
            product_dict = dict()
            product_dict['product_name'] = product[i].product_name
            product_dict['sku'] = product[i].sku
            product_dict['item_name'] = product[i].description
            product_dict['color'] = product[i].color
            array.append(product_dict)
    return Response(array,status=HTTP_200_OK)


@api_view(['GET'])
def ProductDetailView(request, code):
    try:
        product = Product.objects.get(sku=code)
    except Product.DoesNotExist:
         return Response(status=HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
   
   
class AddTransactionView(generics.CreateAPIView):
    queryset = TransactionItem.objects.all()
    serializer_class = TransactionItemSerializer
    # permission_classes = [IsAuthenticated, IsCashier]
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


# ### SALESMAN VIEW
# class AddSalesmanView(generics.ListCreateAPIView):
#     queryset = Salesman.objects.all()
#     serializer_class = AddSalesmanSerializer
#     pagination_class = None
@api_view(['POST', 'GET'])
def AddSalesmanView(request):
    if request.method == 'POST':
        serializer = PostSalesmanSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
            except Exception as e:
                # Log or return detailed exception information
                return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        salesman = Salesman.objects.all()
        serializer = AddSalesmanSerializer(salesman, many=True) 
        return Response(serializer.data, status=HTTP_200_OK)

class GetSalesmanView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Salesman.objects.all()
    serializer_class = PostSalesmanSerializer
    pagination_class = None
    
@api_view(['GET'])
def GetOutletWiseSalesmanView(request, outlet_id):
    try:
        get_outlet = Outlet.objects.get(id=outlet_id)
    except Outlet.DoesNotExist: 
        return Response(status=HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        salesmen = Salesman.objects.filter(salesmanoutlet__outlet_id=outlet_id).prefetch_related('salesmanoutlet')
        salesman_names = salesmen.values('salesman_code','salesman_name')
        return Response(salesman_names, status=HTTP_200_OK)
    
class AddCustomerInPOSView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = AddCustomerInPOSSerializer
    
    

### PAYMENT VIEW
class AddPaymentView(generics.ListCreateAPIView):
    serializer_class = AddPaymentMethodSerializer
    pagination_class = None
    def get_queryset(self):
        shop_id = self.kwargs.get('shop')
        payment_method = PaymentMethod.objects.filter(shop_id=shop_id)
        return payment_method
    

class GetPaymentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddPaymentMethodSerializer
    def get_queryset(self):
        shop_id = self.kwargs.get('shop')
        payment_method = PaymentMethod.objects.filter(shop_id=shop_id)
        return payment_method


### TRANSACTION RETURN VIEW
class TransactionReturnView(generics.CreateAPIView):
    queryset = TransactionReturn.objects.all()
    serializer_class = TransactionReturnSerializer
    pagination_class = None


@api_view(['GET'])
def GetAllInvoicesView(request, outlet):
    # Invoices = Transaction.objects.filter(outlet_code_id=outlet, quantity__gt=0).values('invoice_code').order_by('invoice_code')
    Invoices = (
    Transaction.objects.annotate(
        quantity_as_float=Cast('quantity', FloatField())
    )
    .filter(outlet_code_id=outlet, quantity_as_float__gt=0)
    .values('invoice_code')
    .order_by('invoice_code')
)
    invoices_array = []
    for invoice in Invoices:
            try:
                # Safely split the invoice code
                split_invoice_code = invoice['invoice_code'].split('-')[1]
                invoices_array.append({
                    'invoice': f"Invoice #: {split_invoice_code}",
                    'invoice_code': invoice['invoice_code']
                })
            except IndexError:
            # Handle cases where invoice_code format is invalid
                continue
    return Response(invoices_array)



@api_view(['GET'])    
def GetInvoiceProductsView(request, code):
    cursor = connections['default'].cursor()
    query = "select pr.sku, product_name, description || ' ' || color as items from tbl_transaction_item tri INNER JOIN tbl_product pr on tri.sku = pr.sku where invoice_code_id = '"+ code +"'"
    cursor.execute(query)
    invoice_products = DistinctFetchAll(cursor)
    if len(invoice_products) > 0:
        return Response(invoice_products)
    return Response([], status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
def GetProductDetailView(request, code, sku):
    cursor = connections['default'].cursor()
    query = "select sku, quantity, rate, gross_total,per_discount, discounted_value, item_total from tbl_transaction_item where sku = '"+ sku +"' and invoice_code_id = '"+ code +"'"
    cursor.execute(query)
    invoice_products = DistinctFetchAll(cursor)
    array = []
    if len(invoice_products) > 0:
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
    return Response([], status=HTTP_404_NOT_FOUND)


### DUE RECEIVABLE VIEWS
@api_view(['GET'])
def GetDueInvoicesView(request, outlet):
    transactions = Transaction.objects.filter(outlet_code_id=outlet, due_amount__gt=0).values('invoice_code').order_by('invoice_code')
    due_payment_array = []
    for transaction in transactions:
            try:
                # Safely split the invoice code
                split_invoice_code = transaction['invoice_code'].split('-')[1]
                due_payment_array.append({
                    'invoice': f"Invoice #: {split_invoice_code}",
                    'invoice_code': transaction['invoice_code']
                })
            except IndexError:
            # Handle cases where invoice_code format is invalid
                continue
    return Response(due_payment_array)


@api_view(['GET'])
def GetDueInvoiceAmountView(request, invoice_code):
    try:
        due_amount = Transaction.objects.get(invoice_code=invoice_code).due_amount
    except Transaction.DoesNotExist:
       return Response(status=HTTP_404_NOT_FOUND)
    return Response({"due_amount": due_amount})


@api_view(['PUT'])
def ReceiveDueInvoiceView(request, invoice_code):
    try:
        transaction =Transaction.objects.get(invoice_code=invoice_code)
    except Transaction.DoesNotExist:
          return Response("Invalid Transaction Id" ,status=HTTP_404_NOT_FOUND)
      
    due_amount = request.data.get('due_amount')
    if due_amount > int(transaction.due_amount):
         return Response("The Amount You Enter is greater than due amount" ,status=HTTP_400_BAD_REQUEST)
    if due_amount < 0:
         return Response("Due Amount Cannot Be Negative" ,status=HTTP_400_BAD_REQUEST)
    due = int(transaction.due_amount) - due_amount
    total_pay = int(transaction.total_pay) + due_amount 
    if due == 0:
        advance = 0
        status = "paid"
    else:
        advance = int(transaction.advanced_payment) + due_amount
        status = "unpaid" 
    transaction.due_amount = due
    transaction.advanced_payment = advance
    transaction.total_pay = total_pay
    transaction.status = status
    transaction.save()
    return Response("Due Amount Update")

@api_view(['GET'])
def TodaySaleReportView(request, outlet_id):
    try:
        get_outlet = Outlet.objects.get(id=outlet_id)
    except Outlet.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    today = date.today()
    today_report = Transaction.objects.filter(outlet_code_id=outlet_id, created_at__date=today).select_related('cust_code__customer_type', 'salesman_code')
    today_sale_report = []
    for report in today_report:
        invoice_code = report.invoice_code
        transaction_return =TransactionReturn.objects.filter(invoice_code_id=invoice_code).aggregate(total_return=Coalesce(Sum('rate'),0))
    
        today_sale_report.append({
            'invoice': report.invoice_code.split('-')[1],
            'invoice_code': invoice_code,
            'customer': report.cust_code.customer_type.customer_type if report.cust_code.customer_type else None,
            'salesman': report.salesman_code.salesman_name,
            'total_amount': int(report.grand_total),
            'return_amount':  transaction_return["total_return"],
            'total': int(report.grand_total) - transaction_return["total_return"]
        })
    return Response(today_sale_report)
  




            

    
    
    
    

    
    
