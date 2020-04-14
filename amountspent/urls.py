from django.urls import re_path,path
from amountspent import views

app_name = 'amountspent'

urlpatterns = [
    re_path(r'^$', views.index , name= 'index'),
    path(r'thanks/<total_val>/<total_count>/<start_date>/<end_date>/', views.thanks, name = 'thanks'),
    path(r'error/<date_diff>/',views.date_error, name='date_error')

]