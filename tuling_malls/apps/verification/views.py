from django.shortcuts import render
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
# Create your views here.
from django.http import JsonResponse,HttpResponse
from django.views import View
class image_code_id(View):
    def get(self,request,image_code_id):
        id,image=captcha.captcha.generate_captcha()
        code=get_redis_connection('code')
        code.setex(image_code_id,300,id)
        return HttpResponse(image,content_type='image/jpeg')
class sms_codes(View):
    def get(self,request,mobile):
        image_code =request.GET.get('image_code').lower()
        image_code_id =request.GET.get('image_code_id')
        code=get_redis_connection('code')
        mobiles='tuling'+str(mobile)
        if code.get(image_code_id)==None:
            return JsonResponse({'code': 400, 'err': '图片验证码过期'})
        print(code.get(image_code_id).decode().lower(),image_code)
        if code.get(image_code_id).decode().lower()!=image_code:
            return JsonResponse({'code': 400, 'err': '图片验证码错误'})
        if code.get(mobiles)!=None:
            return JsonResponse({'code': 400, 'err': '请勿在60内重复发送'})
        from libs.yuntongxun.yuntongxun.sms import CCP
        from random import randint
        yzm=str('%06d' % randint(0, 999999))
        print(mobile,code.get(image_code_id).decode().lower(),yzm)
        from celery_tasks.sms.tasks import ytx
        ytx(mobile,yzm)
        codes=code.pipeline()
        codes.setex(mobiles,60,1)
        codes.setex(mobile, 300, yzm)
        codes.execute()
        return JsonResponse({'code': 0, 'err': 'ok'})