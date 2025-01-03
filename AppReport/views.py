# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.generics import *

# from rest_framework.decorators import api_view
# from django.db import connections
# from rest_framework.response import Response
# from django.http import JsonResponse, HttpResponse
# import json
# from AppPOS.models import *
# from AppCustomer.utils import DistinctFetchAll
# from django.db.models import Sum, FloatField
# from django.db.models.functions import Cast




# @api_view(['GET'])
# def GetAllOutletDateView(request, outlet_code):
#     cursor = connections['default'].cursor()
#     query = "select distinct created_at::date from tbl_transaction where outlet_code_id = '" + outlet_code + "'"
#     cursor.execute(query)
#     daily_report = DistinctFetchAll(cursor)
#     return Response(daily_report)



# @api_view(['GET'])
# def DailySaleView(request, outlet_code, date):
#     try:
#         print(outlet_code)
#         print(date)
#         cursor = connections['default'].cursor()
#         # query = "select invoice_code , trans.created_at , ol.outlet_name , cus.customer_type_id as customer_type, sum(grand_total::INTEGER) as total from tbl_transaction as trans INNER JOIN tbl_customer as cus on cus.cust_code = trans.cust_code_id INNER JOIN tbl_outlet as ol on ol.id = trans.outlet_code_id where trans.created_at::date = '" + date + "' and ol.id = '" + outlet_code + "' GROUP BY  invoice_code , trans.created_at ,  ol.outlet_name,  cus.customer_type_id"
#         query = "SELECT trans.invoice_code, trans.created_at, ol.outlet_name, cus.customer_type_id AS customer_type, SUM(trans.grand_total::INTEGER) AS total_amount, COALESCE(ret.total_return, 0) AS return_amount , SUM(trans.grand_total::INTEGER) - COALESCE(ret.total_return, 0) as total  FROM tbl_transaction AS trans INNER JOIN tbl_customer AS cus ON cus.cust_code = trans.cust_code_id INNER JOIN tbl_outlet AS ol ON ol.id = trans.outlet_code_id LEFT JOIN (SELECT invoice_code_id, SUM(total_amount::INTEGER) AS total_return FROM tbl_transaction_return GROUP BY invoice_code_id ) AS ret ON trans.invoice_code = ret.invoice_code_id WHERE trans.created_at::date = '"+ date +"' AND ol.id = '"+ outlet_code +"'GROUP BY trans.invoice_code, trans.created_at, ol.outlet_name, cus.customer_type_id, ret.total_return;"
#         cursor.execute(query)
#         daily_report = DistinctFetchAll(cursor)
#         return Response(daily_report)
#         return Response(daily_report if daily_report else [])
#     except Exception as e:
#              return Response({"error": str(e)}, status=500)


# @api_view(['GET'])
# def DailySaleDetailView(request, invoice_code):
#     cursor = connections['default'].cursor()
#     query = "select invoice_code, quantity, gross_total, discounted_value, items_discount, grand_total, payment_type, tr.status, customer_type_id , tr.created_at::date from tbl_transaction tr INNER JOIN tbl_customer cus on cus.cust_code = tr.cust_code_id  where invoice_code = '" + invoice_code + "'"
#     cursor.execute(query)
#     transaction = DistinctFetchAll(cursor)

#     query_item = "select tr_item.quantity, rate as per_rate, tr_item.gross_total, tr_item.discounted_value, item_total  from tbl_transaction tr INNER JOIN tbl_transaction_item tr_item on tr.invoice_code = tr_item.invoice_code_id  where invoice_code = '" + invoice_code + "'"
#     cursor.execute(query_item)
#     transaction_item = DistinctFetchAll(cursor)
 

#     data_dict = dict()
#     if len(transaction) > 0:
#         data_dict["customer_type"] = transaction[0]["customer_type_id"]
#         data_dict["date"] = str(transaction[0]["created_at"])
#         data_dict["gross_total"] = transaction[0]["gross_total"]
#         data_dict["discount"] = transaction[0]["discounted_value"]
#         data_dict["grand_total"] = transaction[0]["grand_total"]
#         data_dict["status"] = transaction[0]["status"]
#         data_dict["items"] = []

#         for x in range(len(transaction_item)):
#             data_dict["items"].append(transaction_item[x])
#     return Response(data_dict)
 


# @api_view(['GET'])
# def SalesReportView(request, start_date, end_date):
#     cursor = connections['default'].cursor()
#     query = "select sum(grand_total::INTEGER) as total_sale, created_at::date as till_date from tbl_transaction  where created_at::date between '" + start_date + "' and '" + end_date + "' group by till_date order by  till_date DESC"
#     cursor.execute(query)
#     report = DistinctFetchAll(cursor)

#     sales_report = []
#     total = 0
#     if len(report) > 0:
#         for x in range(len(report)):
#             data_dict = dict()
#             data_dict["till_date"] = str(report[x]["till_date"])
#             data_dict["total_sale"] = report[x]["total_sale"]
#             total += int(report[x]["total_sale"])
#             sales_report.append(data_dict)
#         data_dict = dict()
#         data_dict["total"] = total
#         sales_report.append(data_dict)

#     return Response(sales_report)



# @api_view(['GET'])
# def ProfitReportView(request, outlet_code, date):
#     cursor = connections['default'].cursor()
#     # query = "select invoice_code_id, tr_item.sku as sku, product_name, quantity, cost_price,  quantity::INTEGER*cost_price::INTEGER as total_cost , selling_price, quantity::INTEGER*selling_price::INTEGER as total ,quantity::INTEGER*selling_price::INTEGER -  quantity::INTEGER*cost_price::INTEGER as profit   from tbl_transaction_item tr_item INNER JOIN tbl_product pr on tr_item.sku = pr.sku"
#     query = "select invoice_code, tr_item.sku as sku, product_name,tr.created_at, outlet_code_id, tr_item.quantity, cost_price,  tr_item.quantity::INTEGER*cost_price::INTEGER as total_cost , selling_price, tr_item.quantity::INTEGER*selling_price::INTEGER as total ,tr_item.quantity::INTEGER*selling_price::INTEGER -  tr_item.quantity::INTEGER*cost_price::INTEGER as profit from tbl_transaction_item tr_item INNER JOIN tbl_product pr on tr_item.sku = pr.sku inner join tbl_transaction tr on tr_item.invoice_code_id = tr.invoice_code where outlet_code_id ='"+ outlet_code +"' and tr.created_at::date = '"+ date +"' order by invoice_code"
#     cursor.execute(query)
#     report = DistinctFetchAll(cursor)

#     profit_report = []
#     TotalQuantity = 0
#     TotalCost = 0
#     Total = 0
#     Profit = 0
#     if len(report) > 0:
#         for x in range(len(report)):
#             data_dict = dict()
#             data_dict["invoice_code"] = report[x]["invoice_code"]
#             data_dict["sku"] = report[x]["sku"]
#             data_dict["product_name"] = report[x]["product_name"]
#             data_dict["quantity"] = report[x]["quantity"]
#             data_dict["cost_price"] = report[x]["cost_price"]
#             data_dict["total_cost"] = report[x]["total_cost"]
#             data_dict["selling_price"] = report[x]["selling_price"]
#             data_dict["total"] = report[x]["total"]
#             data_dict["profit"] = report[x]["profit"]

#             TotalQuantity += int(report[x]["quantity"])
#             TotalCost += int(report[x]["total_cost"])
#             Total += int(report[x]["total"])
#             Profit += int(report[x]["profit"])
#             profit_report.append(data_dict)

#         data_dict = dict()
#         data_dict["TotalQuantity"] = TotalQuantity
#         data_dict["TotalCost"] = TotalCost
#         data_dict["Total"] = Total
#         data_dict["Profit"] = Profit
#         profit_report.append(data_dict)

#     return Response(profit_report)
  

from rest_framework.generics import *
from rest_framework.decorators import api_view, permission_classes
from django.db import connections
from rest_framework.response import Response
from AppPOS.models import *
from AppCustomer.utils import DistinctFetchAll
from rest_framework.status import *
from django.db.models.functions import TruncDate
from rest_framework.permissions import IsAuthenticated
# from .permissions import * 
from .serializer import *
from datetime import datetime
from django.db.models import Sum, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.db.models import F


# @api_view(['GET'])
# def GetAllOutletDateView(request, outlet):
#     try:
#         outlet = Outlet.objects.get(id=outlet)
#     except Outlet.DoesNotExist:
#         return Response(status=HTTP_404_NOT_FOUND)
#     cursor = connections['default'].cursor()
#     query = "select distinct created_at::date from tbl_transaction where outlet_code_id = '" + outlet + "'"
#     cursor.execute(query)
#     daily_report = DistinctFetchAll(cursor)
#     return Response(daily_report)


@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsReportUser])
def GetAllOutletDateView(request, outlet):
    try:
        outlet = Outlet.objects.get(id=outlet)
    except Outlet.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    daily_report = (
        Transaction.objects.filter(outlet_code_id=outlet)
        .annotate(date=TruncDate('created_at'))
        .values_list('date', flat=True)
        .distinct()
    )
    return Response({"dates": list(daily_report)})



@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsReportUser])
def DailySaleView(request, outlet, date):
    try:
        cursor = connections['default'].cursor()
        # query = "select invoice_code , trans.created_at , ol.outlet_name , cus.customer_type_id as customer_type, sum(grand_total::INTEGER) as total from tbl_transaction as trans INNER JOIN tbl_customer as cus on cus.cust_code = trans.cust_code_id INNER JOIN tbl_outlet as ol on ol.id = trans.outlet_code_id where trans.created_at::date = '" + date + "' and ol.id = '" + outlet_code + "' GROUP BY  invoice_code , trans.created_at ,  ol.outlet_name,  cus.customer_type_id"
        query = "SELECT trans.invoice_code, trans.created_at::date, ol.outlet_name, cus.customer_type_id AS customer_type, SUM(trans.grand_total::INTEGER) AS total_amount, COALESCE(ret.total_return, 0) AS return_amount , SUM(trans.grand_total::INTEGER) - COALESCE(ret.total_return, 0) as total  FROM tbl_transaction AS trans INNER JOIN tbl_customer AS cus ON cus.cust_code = trans.cust_code_id INNER JOIN tbl_outlet AS ol ON ol.id = trans.outlet_code_id LEFT JOIN (SELECT invoice_code_id, SUM(total_amount::INTEGER) AS total_return FROM tbl_transaction_return GROUP BY invoice_code_id ) AS ret ON trans.invoice_code = ret.invoice_code_id WHERE trans.created_at::date = '"+ date +"' AND ol.id = '"+ outlet +"'GROUP BY trans.invoice_code, trans.created_at, ol.outlet_name, cus.customer_type_id, ret.total_return;"
        cursor.execute(query)
        daily_report = DistinctFetchAll(cursor)
        return Response(daily_report if daily_report else [])
    except Exception as e:
             return Response({"error": str(e)}, status=500)

@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsReportUser])
def DailySaleDetailView(request, invoice_code):
    # cursor = connections['default'].cursor()
    # query = "select invoice_code, quantity, gross_total, discounted_value, items_discount, grand_total, payment_type, tr.status, customer_type_id , tr.created_at::date from tbl_transaction tr INNER JOIN tbl_customer cus on cus.cust_code = tr.cust_code_id  where invoice_code = '" + invoice_code + "'"
    # cursor.execute(query)
    # transaction = DistinctFetchAll(cursor)
    
    # query_item = "select tr_item.quantity, rate as per_rate, tr_item.gross_total, tr_item.discounted_value, item_total  from tbl_transaction tr INNER JOIN tbl_transaction_item tr_item on tr.invoice_code = tr_item.invoice_code_id  where invoice_code = '" + invoice_code + "'"
    # cursor.execute(query_item)
    # transaction_item = DistinctFetchAll(cursor)
    try:
        transaction = Transaction.objects.select_related('cust_code__customer_type').get(invoice_code=invoice_code)
    except Transaction.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    transaction_items = TransactionItem.objects.filter(invoice_code_id=invoice_code)
    transaction_return = TransactionReturn.objects.filter(invoice_code_id=invoice_code)

    data_dict = dict()
    data_dict["customer_type"] = transaction.cust_code.customer_type.customer_type if transaction.cust_code.customer_type else None
    data_dict["date"] = transaction.created_at.date()
    data_dict["gross_total"] = transaction.gross_total
    data_dict["discount"] = transaction.discounted_value
    data_dict["grand_total"] = transaction.grand_total
    data_dict["status"] = transaction.status
    data_dict["items"] = []
    data_dict["returns"] = []
    data_dict["Payment"] = []
    transaction_payment = TransactionPayment.objects.filter(transaction_id=transaction.id).select_related('payment')
    for payment in transaction_payment:
        data_dict["Payment"].append({
            "payment_method": payment.payment.pm_name if payment.payment else None,
            "amount": payment.amount,
        })
    ## CREATE A MAP OF SKU THAT USE IN BELOW BOTH LOOPS
    product_map = {
        product.sku : product for product in Product.objects.filter(sku__in=[item.sku for item in transaction_items])
    }
    ### TRANSACTION ITEMS 
    for item in transaction_items:
        product = product_map.get(item.sku)
        data_dict["items"].append({
            "sku": item.sku,
            "product": product.product_name if product else None,
            "variation": product.description if product else None,
            "quantity": item.quantity,
            "per_rate": item.rate,
            "gross_total": item.gross_total,
            "discounted_value": item.discounted_value,
            "item_total": item.item_total,
        })  
    ### TRANSACTION RETURNS
    for returns in transaction_return:
        product = product_map.get(item.sku)
        data_dict["returns"].append({
            "product": product.product_name if product else None ,
            "variation": product.description if product else None,
            "quantity": returns.quantity,
            "per_rate": returns.rate,
            "item_total": returns.total_amount,
        })
    return Response(data_dict)
 

from django.db.models import Sum, F
from django.db.models.functions import Cast, TruncDate
from django.db.models import IntegerField

@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsReportUser])
def SalesReportView(request,outlet, start_date, end_date):
   
    parsed_start_date = datetime.strptime(start_date, '%Y-%m-%d')
    parsed_end_date = datetime.strptime(end_date, '%Y-%m-%d')
    # transactions = (
    # Transaction.objects.filter(created_at__date__range=[parsed_start_date, parsed_end_date])
    # .annotate(till_date=TruncDate('created_at'))
    # .values('till_date')
    # .annotate(total_sale=Sum(F('grand_total')))
    # .order_by('-till_date')
    # )
    transactions = (
    Transaction.objects.filter(created_at__date__range=[parsed_start_date, parsed_end_date], outlet_code_id=outlet)
    .annotate(till_date=TruncDate('created_at'))
    .annotate(grand_total_casted=Cast(F('grand_total'), output_field=IntegerField()))
    .values('till_date')
    .annotate(total_sale=Sum('grand_total_casted'))
    .order_by('-till_date')
)
    return Response(transactions)


@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsReportUser])
def ProfitReportView(request, outlet, date):
    cursor = connections['default'].cursor()
    query = "select invoice_code, tr_item.sku as sku, product_name,tr.created_at, outlet_code_id, tr_item.quantity, cost_price,  tr_item.quantity::INTEGER*cost_price::INTEGER as total_cost , selling_price, tr_item.quantity::INTEGER*selling_price::INTEGER as total ,tr_item.quantity::INTEGER*selling_price::INTEGER -  tr_item.quantity::INTEGER*cost_price::INTEGER as profit, COALESCE(rtn.rate,0) as return_rate, COALESCE(rtn.quantity,0) as return_quantity, COALESCE(rtn.total_amount,0) as return_total from tbl_transaction_item tr_item  INNER JOIN tbl_product pr on tr_item.sku = pr.sku inner join tbl_transaction tr on tr_item.invoice_code_id = tr.invoice_code left JOIN tbl_transaction_return rtn on rtn.invoice_code_id = tr.invoice_code and rtn.sku = tr_item.sku where outlet_code_id ='"+ outlet +"' and tr.created_at::date = '"+ date +"' order by invoice_code"
    cursor.execute(query)
    report = DistinctFetchAll(cursor)

    profit_report = []
    TotalQuantity = 0
    TotalCost = 0
    Total = 0
    Profit = 0
    if len(report) > 0:
        for x in range(len(report)):
            data_dict = dict()
            data_dict["invoice_code"] = report[x]["invoice_code"]
            data_dict["sku"] = report[x]["sku"]
            data_dict["product_name"] = report[x]["product_name"]
            data_dict["quantity"] = report[x]["quantity"]
            data_dict["cost_price"] = report[x]["cost_price"]
            data_dict["total_cost"] = report[x]["total_cost"]
            data_dict["selling_price"] = report[x]["selling_price"]
            data_dict["total"] = report[x]["total"]
            data_dict["profit"] = report[x]["profit"]
            data_dict["return_rate"] = report[x]["return_rate"]
            data_dict["return_quantity"] = int(report[x]["return_quantity"])
            data_dict["return_total"] = report[x]["return_total"]
            profit_report.append(data_dict)
    return Response(profit_report)
  
@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsReportUser])
def OutletWiseSalesmanView(request, outlet): 
    ## CHECK THAT OUTLET EXISTS
    try:
        outlet =Outlet.objects.get(id=outlet)
    except Outlet.DoesNotExist:
        return Response("Outlet Not Found", status=HTTP_404_NOT_FOUND)
    salesman = Salesman.objects.filter(outlet_id=outlet)
    serializer = SalesmanSerializer(salesman, many=True)
    return Response(serializer.data)
  
  
@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsReportUser])  
def SalesmanCommissionReportView(request, outlet, salesman, start_date, end_date):
    ## CHECK THAT OUTLET EXISTS
    try:
        outlet =Outlet.objects.get(id=outlet)
    except Outlet.DoesNotExist:
        return Response("Outlet Not Found", status=HTTP_404_NOT_FOUND)
    ## CHECK THAT SALESMAN EXISTS
    try:
       get_salesman_commission = Salesman.objects.get(salesman_code=salesman)
    except Salesman.DoesNotExist:
        return Response("Salesman Not Found", status=HTTP_404_NOT_FOUND)
    
    ## VALIDATE DATE RANGE
    try:
        get_start_date = datetime.strptime(start_date, '%Y-%m-%d')
        get_end_date =  datetime.strptime(end_date, '%Y-%m-%d')
        if start_date > end_date:
            return Response("Invalid date range", status=HTTP_400_BAD_REQUEST)
    except ValueError:
          return Response("Invalid date format", status=HTTP_400_BAD_REQUEST) 
    transaction_items = TransactionItem.objects.filter(invoice_code__outlet_code_id=outlet, invoice_code__salesman_code_id=salesman,
                                                        created_at__date__range=(get_start_date, get_end_date)).order_by('invoice_item_code')
    
    ## CREATE A MAP OF SKU THAT USE IN BELOW LOOP
    product_map = {
    product.sku: product for product in Product.objects.filter(sku__in=[item.sku for item in transaction_items])
    }
    
    report_array = []
    for items in transaction_items:
   
        product = product_map.get(items.sku)
        salesman_per = int(get_salesman_commission.retail_commission)
        total_commission =  int(int(items.item_total) / 100 * salesman_per)
        report_array.append({
            "till_date": items.created_at.date(),
            "invoice": items.invoice_code_id,
            "sku": items.sku,
            "product": product.product_name if product else None,
            "quantity": items.quantity,
            "Price": items.rate,
            "gross_total": items.gross_total,
            "discount": items.discounted_value,
            "total": items.item_total,
            "Per(%)": salesman_per,
            "Commission": total_commission,
        })
    return Response(report_array)