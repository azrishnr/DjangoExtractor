from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from .models import URL
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests, bs4

def index(requests):
    if(requests.method == 'POST'):
        links = URL.objects.all()[:]
        if(extract(links)==True):
            message = 'Extracted sucessfully to sheet!'
            context = {
                'message': message
             }
            return render(requests, 'htags/index.html', context)
        else:
            message = 'error'
            context = {
                'message': message
            }
            return render(requests, 'htags/index.html', context)
    else:
        urls = URL.objects.all()[:]
        context = {
            'urls': urls
        }
        return render(requests, 'htags/index.html', context)

def add(request):
    if(request.method == 'POST'):
        url_text = request.POST['hdrurl']
        try:
            URLValidator()(url_text)
        except ValidationError:
            return render(request, 'htags/add.html', {
                'error_message': "Enter a valid URL",
            })
        url = URL(url_text=url_text)
        url.save()
        return redirect('/htags')
    else:
        return render(request, 'htags/add.html')


def extract(urllist):
    scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('htags/client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Bulk Meta Tag Extractor').sheet1

    hds = ['h1','h2','h3','h4','h5','h6']

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'} 

    clearsheet(sheet)
    
    for i in range(len(urllist)):
        sheet.update_cell(i+2,1,str(urllist[i]))
    
    for i in range(len(urllist)): 
        result = urllist[i] 

        # read header of each url
        res = requests.get(result, headers=headers)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        
        for j in range(6):
            helem = soup.select(hds[j])
            num = len(helem)
            cellupdate = ''
            for k in range(num):
                cellupdate += helem[k].getText() + '\n'
            newcell = cellupdate.strip()
            sheet.update_cell(i+2,j+2,newcell)
    return True 


def clearsheet(sheet):
    cell_list = sheet.range('A2:I'+ str(len(sheet.row_values(1))+2))

    for cell in cell_list:
        cell.value = ''
    
    sheet.update_cells(cell_list)    
