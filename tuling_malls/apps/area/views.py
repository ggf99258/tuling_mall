from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from utils.views import LoginRequiredMixin_2
from django.views import View
from .models import Area
from django.core.cache import cache
class areas(LoginRequiredMixin_2,View):
    def get(self,request):
        caches = cache.get('province_list')
        if caches is None:
            areas=Area.objects.filter(parent=None).all()
            province_list=[]
            for i in areas:
                province_list.append({
                    'id':i.id,
                    'name':i.name
                })
            cache.set('province_list',province_list,3600*24)
        return JsonResponse({'code':0,'erring':'ok','province_list':caches})
class areas_id(LoginRequiredMixin_2,View):
    def get(self,request,id):
        caches=cache.get(id)
        if caches is None:
            areas = Area.objects.filter(parent=id).all()
            subs = []
            for i in areas:
                subs.append({
                    'id': i.id,
                    'name': i.name
                })
            cache.set(id,subs,3600*24)
        sub_data={'subs':caches}
        return JsonResponse({'code': 0, 'erring': 'ok', 'sub_data': sub_data})