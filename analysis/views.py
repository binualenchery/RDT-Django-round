# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import StockName, StockPrices
from django.shortcuts import render
from django.db import connection

def microsoft(request):
    cursor = connection.cursor()
    
    # Getting data from db
    cursor.execute("""SELECT id, stock_date, stock_open, stock_close
    FROM analysis_stockprices
    WHERE stock_id_id='1' ORDER BY stock_date""")
    data = cursor.fetchall()
    data = list(list(d) for d in data)
    prev_close = None
    dat1 = [] # dat1 is appended with processed data along with percentage change
    for d in data:
        
        dct = dict()
        
        dct['open'] = d[2]
        dct['close'] = d[3]
        if prev_close is None:
            per_change = ''
        else:
            per_change = round((d[3]-prev_close)/prev_close * 100,2)
        prev_close = d[3]
        dct['per_change'] = per_change
        dct['date'] = d[1].strftime("%b %d, %Y")
        
        dat1.append(dct)
        
    # Getting volume data from db     
    cursor.execute("""SELECT id, stock_date, stock_volume
    FROM analysis_stockprices
    WHERE stock_id_id='1' ORDER BY stock_volume DESC LIMIT 5""")
    data = cursor.fetchall()
    data = list(list(d) for d in data)
    dat2 = [] # dat2 is appended with volume data
    for d in data:
        dat2.append({'date':d[1].strftime("%b %d, %Y"), 'volume':d[2]})
                
    context = {'microsoft':{'dat1':dat1,'dat2':dat2}}
    
    return render(request, 'microsoft/microsoft.html',context)
