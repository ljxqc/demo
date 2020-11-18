from django.shortcuts import render, HttpResponse, redirect
import csv
from index.models import Product
from django.views.generic import ListView
# Create your views here.


def index(request):
    # return HttpResponse('Hello World !')
    # return render(request, 'index.html', context={'title': '首页'}, status=500)
    # type_list = Product.objects.values('type').distinct()
    # name_list = Product.objects.values('name', 'type')
    # context = {'title': '首页', 'type_list': type_list, 'name_list': name_list}
    # return render(request, 'index.html', context=context, status=200)
    # return HttpResponse(str(2111))

    type_list = Product.objects.values('type').distinct()
    name_list = Product.objects.values('name', 'type')
    title = '首页'
    return render(request, 'index.html', context=locals(), status=200)  # 用locals() 代替context

def temp_inherit(request):
    return render(request, 'index_temp_inherit.html')

def defined_filter(request):

    return render(request, 'index_filter.html', context={'title': '首页'})

def mydate(request, year, month, day):
    return HttpResponse(f'{str(year)}/{str(month)}/{str(day)}')


def myyear(request, year):
    return render(request, 'myyear.html')

def myyear_dict(request, year, month):
    return render(request, 'myyear_dict.html', {'month': month})

def download(request):
    response = HttpResponse(content_type='text?csv')
    response['Content-Disposition'] = 'attachment;filename="somefilename.csv"'
    wirter = csv.writer(response)
    wirter.writerow(['First row', 'A', 'B', 'C'])
    return response

def login(request):
    # return redirect('/')
    if request.method =='POST':
        name = request.POST.get('name')
        return redirect('/')
    else:
        if request.GET.get('name'):
            name = request.GET.get('name')
        else:
            name = 'Everyone'
        return HttpResponse('username is ' + name)
    # return redirect('http://127.0.0.1:8000/')

# 通用视图
# class ProductList(ListView):
#     context_object_name = 'type_list'
#     template_name = 'index_view.html'
#     queryset = Product.objects.values('type_name').distinct()
#
#     def get_queryset(self):
#         print(self.kwargs['id'])
#         print(self.kwargs['name'])
#         print(self.request.method)
#         type_list = Product.objects.values('type_name').distinct()
#         return type_list
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductList, self).get_context_data(**kwargs)
#         context['name_list'] = Product.objects.values('name', 'type_name')
#         return context


