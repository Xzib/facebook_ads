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
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            x = int(str(end_date - start_date).split()[0])
            if x < 0:
                date_diff = "Start Date must be smaller then End Date"
                return HttpResponseRedirect(reverse('amountspent:date_error', args=(date_diff,)))
            print(x)
            start_date = str(start_date)
            end_date = str(end_date)
            print(f"Your start date is {start_date} and your end date is {end_date}" )
            # print(type(start_date))
            spend = get_data_from_api(start_date,end_date)
            # spend = list(spend)
            list_of_data = spend[1]

            request.session['table_val'] = list_of_data
            request.session['start_date'] = start_date
            request.session['end_date'] = end_date
            print(list_of_data)
            df = pd.DataFrame(spend[0])
            df.columns = ['Campaign_ID', 'Page_ID', 'Amount_spent']
            return HttpResponseRedirect(reverse('amountspent:thanks'))
    else:
        form = AmountDate()
    
    return render(request, 'amountspent/index.html' , {'form' : form})

def thanks(request):
    context = {'table_data':request.session['table_val'], 'start_date':request.session['start_date'], 'end_date':request.session['end_date']}
    return  render(request,'amountspent/thanks.html', context = context)

def date_error(request, date_diff):
    return render(request, 'amountspent/date_error.html',{'error':date_diff})