from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from amountspent.forms import AmountDate
from amountspent.fb_data import get_data_from_api
import pandas as pd
# Create your views here.

def index(request):
    if request.method == 'POST':
        form = AmountDate(request.POST)
        # print(form.start_date)
        # print(form.end_date)
        if form.is_valid():
            start_date = str(form.cleaned_data['start_date'])
            end_date = str(form.cleaned_data['end_date'])
            print(f"Your start date is {start_date} and your end date is {end_date}" )
            print(type(start_date))
            spend = get_data_from_api(start_date,end_date)
            df = pd.DataFrame(spend)
            df.columns = ['Amount_spent']
            df = df.astype(float)
            total_val = df['Amount_spent'].sum()
            total_val = float("{:.2f}".format(total_val))
            total_count = len(df.index)
            return HttpResponseRedirect(reverse('amountspent:thanks', args=(total_val, total_count, start_date, end_date)))
    else:
        form = AmountDate()
    
    return render(request, 'amountspent/index.html' , {'form' : form})

def thanks(request, total_val, total_count, start_date, end_date):
    return  render(request,'amountspent/thanks.html', 
                    {'total_val': total_val, 'total_count': total_count, 
                    'start_date':start_date,'end_date': end_date}
                    )