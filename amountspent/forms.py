from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

class AmountDate(forms.Form):
    start_date = forms.DateField(label = 'Start Date' , widget = DateInput(attrs={'class':'my-4 mx-1 px-4'}))
    end_date = forms.DateField(label = 'End Date', widget = DateInput(attrs={'class':'my-4 mx-1 px-4'}))