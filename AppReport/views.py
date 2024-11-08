from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import *

from rest_framework.decorators import api_view
from django.db import connections
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
import json
from AppPOS.models import *


# Create your views here.
def DictinctFetchAll(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

@api_view(['GET'])
def GetAllOutletDateView(request, code):
    cursor = connections['default'].cursor()
    query = "select distinct created_at::date from tbl_transaction where outlet_code_id = '" + code + "'"
    cursor.execute(query)
    daily_report = DictinctFetchAll(cursor)
    return Response(daily_report)


@api_view(['GET'])
def DailySaleView(request, code):
    split_code = code.split("^^")
    outlet_code = split_code[0]
    date = split_code[1]
    cursor = connections['default'].cursor()
    query = "select invoice_code , trans.created_at , ol.outlet_name , cus.customer_type_id as customer_type, sum(grand_total::INTEGER) as total from tbl_transaction as trans INNER JOIN tbl_customer as cus on cus.cust_code = trans.cust_code_id INNER JOIN tbl_outlet as ol on ol.outlet_code = trans.outlet_code_id where trans.created_at::date = '" + date + "' and ol.outlet_code = '" + outlet_code + "' GROUP BY  invoice_code , trans.created_at ,  ol.outlet_name,  cus.customer_type_id"
    cursor.execute(query)
    daily_report = DictinctFetchAll(cursor)
    return Response(daily_report)


@api_view(['GET'])
def DailySaleDetailView(request, code):
    cursor = connections['default'].cursor()
    query = "select invoice_code, quantity, gross_total, discounted_value, items_discount, grand_total, payment_type, tr.status, customer_type_id , tr.created_at::date from tbl_transaction tr INNER JOIN tbl_customer cus on cus.cust_code = tr.cust_code_id  where invoice_code = '" + code + "'"
    cursor.execute(query)
    transaction = DictinctFetchAll(cursor)

    query_item = "select tr_item.quantity, rate as per_rate, tr_item.gross_total, tr_item.discounted_value, item_total  from tbl_transaction tr INNER JOIN tbl_transaction_item tr_item on tr.invoice_code = tr_item.invoice_code_id  where invoice_code = '" + code + "'"
    cursor.execute(query_item)
    transaction_item = DictinctFetchAll(cursor)
    # return Response(daily_report)

    data_dict = dict()
    if len(transaction) > 0:
        data_dict["customer_type"] = transaction[0]["customer_type_id"]
        data_dict["date"] = str(transaction[0]["created_at"])
        data_dict["gross_total"] = transaction[0]["gross_total"]
        data_dict["discount"] = transaction[0]["discounted_value"]
        data_dict["grand_total"] = transaction[0]["grand_total"]
        data_dict["status"] = transaction[0]["status"]
        data_dict["items"] = []

        for x in range(len(transaction_item)):
            data_dict["items"].append(transaction_item[x])
    return HttpResponse(json.dumps(data_dict))


@api_view(['GET'])
def SalesReportView(request, start_date, end_date):
    cursor = connections['default'].cursor()
    query = "select sum(grand_total::INTEGER) as total_sale, created_at::date as till_date from tbl_transaction  where created_at::date between '" + start_date + "' and '" + end_date + "' group by till_date order by  till_date DESC"
    cursor.execute(query)
    report = DictinctFetchAll(cursor)

    sales_report = []
    total = 0
    if len(report) > 0:
        for x in range(len(report)):
            data_dict = dict()
            data_dict["till_date"] = str(report[x]["till_date"])
            data_dict["total_sale"] = report[x]["total_sale"]
            total += int(report[x]["total_sale"])
            sales_report.append(data_dict)
        data_dict = dict()
        data_dict["total"] = total
        sales_report.append(data_dict)

    return HttpResponse(json.dumps(sales_report))


@api_view(['GET'])
def ProfitReportView(request):
    cursor = connections['default'].cursor()
    query = "select invoice_code_id, tr_item.sku as sku, product_name, quantity, cost_price,  quantity::INTEGER*cost_price::INTEGER as total_cost , selling_price, quantity::INTEGER*selling_price::INTEGER as total ,quantity::INTEGER*selling_price::INTEGER -  quantity::INTEGER*cost_price::INTEGER as profit   from tbl_transaction_item tr_item INNER JOIN tbl_product pr on tr_item.sku = pr.sku"
    cursor.execute(query)
    report = DictinctFetchAll(cursor)

    profit_report = []
    TotalQuantity = 0
    TotalCost = 0
    Total = 0
    Profit = 0
    if len(report) > 0:
        for x in range(len(report)):
            data_dict = dict()
            data_dict["invoice_code"] = report[x]["invoice_code_id"]
            data_dict["sku"] = report[x]["sku"]
            data_dict["product_name"] = report[x]["product_name"]
            data_dict["quantity"] = report[x]["quantity"]
            data_dict["cost_price"] = report[x]["cost_price"]
            data_dict["total_cost"] = report[x]["total_cost"]
            data_dict["selling_price"] = report[x]["selling_price"]
            data_dict["total"] = report[x]["total"]
            data_dict["profit"] = report[x]["profit"]

            TotalQuantity += int(report[x]["quantity"])
            TotalCost += int(report[x]["total_cost"])
            Total += int(report[x]["total"])
            Profit += int(report[x]["profit"])
            profit_report.append(data_dict)


        data_dict = dict()
        data_dict["TotalQuantity"] = TotalQuantity
        data_dict["TotalCost"] = TotalCost
        data_dict["Total"] = Total
        data_dict["Profit"] = Profit
        profit_report.append(data_dict)

    return HttpResponse(json.dumps(profit_report))
