from django.shortcuts import render
from datetime import datetime

def find_year():
    date = datetime.now()
    if date.month==1 and date.day==1:
        return 'Happy New Year'
    else:
        return 'Today isn\'t new year'
def isnewyear(request):
    year = find_year()
    context = {
            "year":datetime.now().month==1 and datetime.now().day==1
            }
    return render(request,'year.html',context)


