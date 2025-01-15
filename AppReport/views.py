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
        query = "SELECT trans.invoice_code, trans.created_at::date, ol.outlet_name, cus.customer_type_id AS customer_type, SUM(trans.grand_total::INTEGER) AS total_amount, COALESCE(ret.total_return, 0) AS return_amount , SUM(trans.grand_total::INTEGER) - COALESCE(ret.total_return, 0) as total  FROM tbl_transaction AS trans INNER JOIN tbl_customer AS cus ON cus.cust_code = trans.cust_code_id INNER JOIN tbl_outlet AS ol ON ol.id = trans.outlet_code_id LEFT JOIN (SELECT invoice_code_id, SUM(total_amount::INTEGER) AS total_return FROM tbl_transaction_return GROUP BY invoice_code_id ) AS ret ON trans.invoice_code = ret.invoice_code_id WHERE trans.quantity::INTEGER > 0 AND trans.created_at::date = '"+ date +"' AND ol.id = '"+ outlet +"'GROUP BY trans.invoice_code, trans.created_at, ol.outlet_name, cus.customer_type_id, ret.total_return;"
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
    data_dict["additional_fee"] = []
    data_dict["Payment"] = []
    transaction_payment = TransactionPayment.objects.filter(transaction_id=transaction.id).select_related('payment')
    for payment in transaction_payment:
        data_dict["Payment"].append({
            "payment_method": payment.payment.pm_name if payment.payment else None,
            "amount": payment.amount,
        })
        
    ## ADDITIONAL FEE    
    transaction_additional_fee = FeeRecord.objects.filter(transaction_id_id=transaction.id).select_related('fee_type')
    for fee in transaction_additional_fee:
        data_dict["additional_fee"].append({
            "fee_method": fee.fee_type.fee_name if fee.fee_type else None,
            "fee": fee.fee,
        })
    ## CREATE
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
    cursor = connections['default'].cursor()
    # transaction = "SELECT tr.created_at::date AS till_date, SUM(tr.grand_total::INTEGER) - COALESCE(SUM(returns.total_return), 0) AS total_sale FROM tbl_transaction tr LEFT JOIN ( SELECT invoice_code_id,  SUM(total_amount) AS total_return FROM tbl_transaction_return GROUP BY invoice_code_id) returns ON tr.invoice_code = returns.invoice_code_id WHERE tr.grand_total::INTEGER > 0 AND tr.outlet_code_id = '"+ outlet +"' AND tr.created_at::date BETWEEN '"+ str(parsed_start_date) +"' AND '"+ str(parsed_end_date) +"' GROUP BY tr.created_at::date ORDER BY till_date	;"
    transaction = "WITH sales AS (SELECT tr.created_at::date AS sale_date, SUM(tr.grand_total::INTEGER) AS total_sale FROM tbl_transaction tr WHERE tr.grand_total::INTEGER > 0 AND tr.outlet_code_id =  '"+ outlet +"' AND tr.created_at::date BETWEEN  '"+ str(parsed_start_date) +"' AND  '"+ str(parsed_end_date) +"' GROUP BY tr.created_at::date),returns AS (SELECT  tr_return.created_at::date AS return_date, SUM(tr_return.total_amount) AS total_return FROM tbl_transaction_return tr_return WHERE tr_return.created_at::date BETWEEN  '"+ str(parsed_start_date) +"' AND  '"+ str(parsed_end_date) +"' GROUP BY tr_return.created_at::date)SELECT COALESCE(sales.sale_date, returns.return_date) AS till_date, COALESCE(sales.total_sale, 0) AS total_sale, COALESCE(returns.total_return, 0) AS total_return, COALESCE(sales.total_sale, 0) - COALESCE(returns.total_return, 0) AS net_sale FROM sales FULL OUTER JOIN  returns ON sales.sale_date = returns.return_date ORDER BY till_date;"
    cursor.execute(transaction)
    report = DistinctFetchAll(cursor)
    return Response(report)


@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsReportUser])
def ProfitReportView(request, outlet, date):
    cursor = connections['default'].cursor()
    query = "select invoice_code, tr_item.sku as sku, product_name,tr.created_at, outlet_code_id, tr_item.quantity, cost_price,  tr_item.quantity::INTEGER*cost_price::INTEGER as total_cost , selling_price, tr_item.quantity::INTEGER*selling_price::INTEGER as total ,tr_item.quantity::INTEGER*selling_price::INTEGER -  tr_item.quantity::INTEGER*cost_price::INTEGER as profit, COALESCE(rtn.rate,0) as return_rate, COALESCE(rtn.quantity,0) as return_quantity, COALESCE(rtn.total_amount,0) as return_total from tbl_transaction_item tr_item  INNER JOIN tbl_product pr on tr_item.sku = pr.sku inner join tbl_transaction tr on tr_item.invoice_code_id = tr.invoice_code left JOIN tbl_transaction_return rtn on rtn.invoice_code_id = tr.invoice_code and rtn.sku = tr_item.sku where outlet_code_id ='"+ outlet +"' and tr.created_at::date = '"+ date +"' and tr_item.quantity::INTEGER > 0 order by invoice_code"
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
    salesman = Salesman.objects.filter(salesmanoutlet__outlet_id=outlet)
    serializer = SalesmanSerializer(salesman, many=True)
    return Response(serializer.data)
  
  
@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsReportUser])  
def SalesmanCommissionReportView(request, outlet, salesman, start_date, end_date):
    ## CHECK THAT OUTLET EXISTS
    try:
        get_outlet =Outlet.objects.get(id=outlet)
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
    # transaction_items = TransactionItem.objects.filter(invoice_code__outlet_code_id=outlet, invoice_code__salesman_code_id=salesman,  quantity__gt=0,
    #                                                     created_at__date__range=(get_start_date, get_end_date)).order_by('invoice_item_code')
    cursor = connections['default'].cursor()
    query = "SELECT *, ti.created_at::date FROM tbl_transaction_item ti INNER JOIN tbl_transaction t ON ti.invoice_code_id = t.invoice_code WHERE t.outlet_code_id = '"+ outlet +"' AND t.salesman_code_id = '"+ salesman +"' AND ti.quantity::INTEGER > 0 AND ti.created_at::date BETWEEN '"+ str(get_start_date) +"' AND '"+ str(get_end_date) +"' ORDER BY ti.invoice_item_code;"
    cursor.execute(query)
    transaction_items = DistinctFetchAll(cursor)
    
    
    
    ## CREATE A MAP OF SKU THAT USE IN BELOW LOOP
    product_map = {
    product.sku: product for product in Product.objects.filter(sku__in=[item["sku"] for item in transaction_items])
    }
    # product_map = {
    # product.sku: product for product in Product.objects.filter(sku__in=[item.sku for item in transaction_items])
    # }
    
    report_array = []
    for items in transaction_items:
        product = product_map.get(items["sku"])
        salesman_per = int(get_salesman_commission.retail_commission)
        total_commission =  int(int(items["item_total"]) / 100 * salesman_per)
        report_array.append({
            "till_date": items['created_at'],
            "invoice": items["invoice_code_id"],
            "sku": items["sku"],
            "product": product.product_name if product else None,
            "quantity": items["quantity"],
            "Price": items["rate"],
            "gross_total": items['gross_total'],
            "discount": items['discounted_value'],
            "total": items['item_total'],
            "Per(%)": salesman_per,
            "Commission": total_commission,
        })
   
        # product = product_map.get(items.sku)
        # salesman_per = int(get_salesman_commission.retail_commission)
        # total_commission =  int(int(items.item_total) / 100 * salesman_per)
        # report_array.append({
        #     "till_date": items.created_at.date(),
        #     "invoice": items.invoice_code_id,
        #     "sku": items.sku,
        #     "product": product.product_name if product else None,
        #     "quantity": items.quantity,
        #     "Price": items.rate,
        #     "gross_total": items.gross_total,
        #     "discount": items.discounted_value,
        #     "total": items.item_total,
        #     "Per(%)": salesman_per,
        #     "Commission": total_commission,
        # })
    return Response(report_array)


from collections import defaultdict

@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsReportUser])
def PaymentMethodReportView(request, outlet,date): 
    try:
        get_outlet = Outlet.objects.get(id=outlet)
    except Outlet.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    transactions = Transaction.objects.filter(created_at__date=date, outlet_code_id=outlet).prefetch_related('payment')
    payment_methods = PaymentMethod.objects.all()

    payment_method_data = [
        {
            'id': pay.id,
            "payment_method": pay.pm_name,
            "amount": 0,
        }
        for pay in payment_methods
    ]

    #### Create a mapping of payment IDs to payment_method_data indices for efficient updates
    payment_id_to_index = {pay['id']: idx for idx, pay in enumerate(payment_method_data)}

    #### Aggregate transaction payments
    transaction_payments = TransactionPayment.objects.filter(transaction__in=transactions)

    #### Use a dictionary to group payment amounts
    payment_totals = defaultdict(int)
    for tp in transaction_payments:
        payment_totals[tp.payment_id] += int(tp.amount)


    for payment_id, total_amount in payment_totals.items():
        if payment_id in payment_id_to_index:
            payment_method_data[payment_id_to_index[payment_id]]["amount"] = total_amount
    return Response(payment_method_data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsReportUser])
def ProductWiseReturnView(request, outlet, date): 
    try:
        get_outlet = Outlet.objects.get(id=outlet)
    except Outlet.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    
    cursor = connections['default'].cursor()
    query = "SELECT * FROM tbl_transaction where quantity::INTEGER < '0' and created_at::date = '"+ date +"' and outlet_code_id = '"+ outlet +"'"
    cursor.execute(query)
    transaction = DistinctFetchAll(cursor)
    transaction_return = []

    for return_item in transaction:
        return_dict = {
            "invoice_code": return_item['invoice_code'],
            "quantity": str(return_item['quantity']).replace("-", ""),  # Ensure it's a string before replacing
            "grand_total": str(return_item['grand_total']).replace("-", ""),  # Ensure it's a string before replacing
        }
        transaction_return.append(return_dict)
    return Response(transaction_return)


@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsReportUser])
def ProductWiseReturnDetailView(request, invoice_code): 
    
    transaction_return = TransactionItem.objects.filter(invoice_code_id=invoice_code)
    product_map = {
        product.sku : product for product in Product.objects.filter(sku__in=[item.sku for item in transaction_return])
    }
    
    transaction_return_detail = []
    for return_item in transaction_return:
        
        product = product_map.get(return_item.sku)
        print(product.product_name)
        quantity =  int(return_item.quantity.replace("-", ""))
        product_dict = dict()
        product_dict["product"] = product.product_name if product else None
        product_dict["variation"] = product.description if product else None
        product_dict["sku"] = return_item.sku
        product_dict["quantity"] = quantity
        product_dict["rate"] = int(return_item.rate)
        product_dict["discount"] = int(return_item.discounted_value.replace("-", ""))
        product_dict["total"] = int(return_item.rate) *  quantity + int(return_item.discounted_value)
        transaction_return_detail.append(product_dict)

    return Response(transaction_return_detail)