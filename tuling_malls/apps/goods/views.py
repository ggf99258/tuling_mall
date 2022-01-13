from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views import View
# Create your views here.
from utils.skus import goods_channel,mianbaoxie,get_goods_specs
from .models import ContentCategory,Content,SKU
class index(View):
    def get(self,request):
        categories=goods_channel()
        content=ContentCategory.objects.all()
        contents={}
        for i in content:
            print(i.id)
            contents[i.key]=Content.objects.filter(category_id=i.id,status=True).order_by('sequence')
        context={
            'categories': categories,
            'contents':contents
        }
        return render(request,'index.html',context)
from haystack.views import  SearchView
class search(SearchView):
    def create_response(self):
        context = self.get_context()
        print(context)
        data_list=[]
        for cat in context['page'].object_list:
            data_list.append({
                'id':cat.object.id,
                'default_image_url':cat.object.default_image.url,
                'name':cat.object.name,
                'searchkey': context.get('query'),
                'price':cat.object.price,
                'count':context['page'].paginator.count,
                'page_size': context['page'].paginator.num_pages
            })
        return JsonResponse(data_list,safe=False)
from django.core.paginator import Paginator
class list_skus(View):
    def get(self,request,id):
        page=request.GET.get('page')
        page_size=request.GET.get('page_size')
        ordering=request.GET.get('ordering')
        sku=SKU.objects.filter(category=id,is_launched=True).order_by(ordering)
        if sku==None:
            return JsonResponse({'code': 400, 'errmsg': '查询失败'})
        skus=Paginator(sku,per_page=page_size)
        skul=skus.page(page)
        count=skus.num_pages
        list=[]
        for cat in skul.object_list:
            list.append({
                'price':cat.price,
                'name':cat.name,
                'id':id,
                'default_image_url':cat.default_image.url
            })
        breadcrumb=mianbaoxie(id)
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'list': list, 'count': count, 'breadcrumb': breadcrumb, 'counts': sku.count()})
class hot_sku(View):
    def get(self,request,id):
        cats=SKU.objects.filter(category=id,is_launched=True).order_by('sales')[:3]
        list=[]
        for cat in cats:
            list.append({
                'price': cat.price,
                'name': cat.name,
                'id': id,
                'default_image_url': cat.default_image.url
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'hot_skus': list})
class goods_id(View):
    def get(self,request,id):
        sku=SKU.objects.get(id=id)
        breadcrumb=mianbaoxie(sku.category_id)
        goods_specs=get_goods_specs(sku)
        categories = goods_channel()
        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'sku': sku,
            'specs': goods_specs
        }
        return render(request,'detail.html',context)
from .models import GoodsCategory,Count_visit
import datetime
class detail_visit(View):
    def post(self,request,id):
        try:
            cat=GoodsCategory.objects.get(id=id)
        except:
            return JsonResponse({'code': 400, 'errmsg': '没有此商品'})
        cat1=GoodsCategory.objects.get(id=cat.parent_id)
        today=datetime.date.today()
        try:
            visit=Count_visit.objects.get(time=today,category_id=cat1.parent)
        except:
            Count_visit.objects.create(
                time=today,
                count=1,
                category=cat1.parent
            )
            return JsonResponse({'code': 0, 'errmsg': 'ok'})
        visit.count += 1
        visit.save()
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
from django_redis import get_redis_connection
import json
