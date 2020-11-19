from django.shortcuts import render, HttpResponse, redirect
import csv
from index.models import *
from django.db.models import Q, F, Count, Sum
from django.db.models.functions import Concat
from django.db.models import Value
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

def sql_crud(request):
    # # 查
    # print(Product.objects.get(id=2))  # 只能查询主键或唯一约束字段，否则报错
    #
    # print(Product.objects.filter(id=2))  #单个查询
    # print(Product.objects.filter(id=9, name='华为荣耀v9'))  # 多个查询 条件
    # # 对条件包裹一层 Q 的时候，filter 支持 "~", "&", "|"
    # print(Product.objects.filter(Q(name='华为荣耀v9') | Q(id=9)))  # or查询
    # print(Product.objects.filter(Q(name='荣耀v9') & ~ Q(id=9)))  # ~ 取非
    # # 查询函数可以混合使用 Q， 但Q 必须位于所有关键字参数前面
    # print(Product.objects.filter(Q(name='荣耀v9'), id=15))  # 混合使用，Q 必须位于位置参数前
    # # # F() 的实例可以在查询中引用字段，来比较同一个 model 实例中两个不同字段的值
    # # Product.objects.filter(id__gt=F('type_id'))  #
    # # # Django 支持 F() 对象之间以及 F() 对象和常数之间的加减乘除和取模的操作
    # # Product.objects.filter(id__gt=F('id')+1)
    # # # 修改 char 字段时需对字符串进行拼接 Concat 操作，且需加上拼接值 value
    # # Product.objects.update(name=Concat(F('name'), Value('新款')))
    # print(Product.objects.filter())  # 查询全部
    # print(Product.objects.filter(name='荣耀v9').count())  # 统计查询数据量
    # print((Product.objects.values('name').filter(type_id=1)).distinct())  # 去重查询
    #
    # print(Product.objects.all())  # 全表查询,
    # print(Product.objects.all()[:5])  # 查询前5个
    # print(Product.objects.values('name'))  # 查询某个字段，返回字典
    # print(Product.objects.values('name', 'weight'))  # 查询某个字段，返回字典
    # print(Product.objects.values_list('name'))  # 查询某个字段，返回列表，列表元素以元组格式表示
    #
    # print(Product.objects.order_by('-id'))  # 排序
    # print(Product.objects.order_by('-id', 'name'))  # 多字段排序
    #
    # # select name, sum(id) as 'id_sum' from index_product group by name
    # print(Product.objects.values('name').annotate(Sum('id')))
    # # select count(id) as 'id_count' from index_product
    # print(Product.objects.aggregate(id_count=Count('id')))

    # # 增
    # Product.objects.create(name='荣耀v9', weight='111g', size='120*75*7mm', type_id=1)  # 类似于 p=Product(name='华为').save()
    # # 改
    # Product.objects.get(id=14).update(name='华为荣耀v9')  # 更新单条数据
    # Product.objects.filter(name='荣耀v9').update(name='华为荣耀v9')  # 更新多条数据
    # Product.objects.update(name='华为荣耀v9')  # 更新全部数据
    # # 删
    # Product.objects.get(id=1).delete()  # 删除单条数据
    # Product.objects.filter(name='华为荣耀v9').delete()  # 删除多条数据
    # Product.objects.all().delete()  # 删除全部数据

    # 一对一，一对多查询
    # 外键查询 select_related()，参数为外键，可多个外键连查，用“__”连接
    t = Type.objects.filter(product__id=9)  # 正向查询
    print(t[0].type_name)
    print(t[0].product_set.values('name'))  # 反向查询
    print(Type.objects.select_related('type').values('product__name', 'product__weight'))
    print(Product.objects.select_related('type').values('name', 'type__type_name'))  # 查询两个模型部分数据
    print(Product.objects.select_related('type').all())  # 查询两个模型全部数据
    print(Product.objects.select_related('type').filter(id__gt=8))  # 查询两个模型数据中Product.id>8 的
    print(Product.objects.select_related('type').filter(type__type_name='手机'))  # 查询两个模型数据中Product.id>8 的
    print(Person.objects.select_related('city__province').get(name='张三'))  # 多个表外键查询




    return HttpResponse('增删改查完毕，请查看结果！')










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


