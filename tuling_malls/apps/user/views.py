from django.shortcuts import render
from .models import User
from django.views import View
from django.http import JsonResponse
from django_redis import get_redis_connection
import json,re
from django.contrib.auth import authenticate,login,logout
# Create your views here.
class usernames(View):
    def get(self,request,username):
        count=User.objects.filter(username=username).count()
        return JsonResponse({'code':0,'errmsg':'ok','count':count})
class mobiles(View):
    def get(self,request,mobile):
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'count': count})
class register(View):
    def post(self,request):
        res=json.loads(request.body)
        print(res)
        username=res.get('username'),
        password=res.get('password'),
        password2=res.get('password2'),
        mobile=res.get('mobile'),
        sms_code=res.get('sms_code'),
        allow=res.get('allow')
        if not all([username,password,password2,mobile,sms_code,allow]):
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})
        if not re.match(r'^[a-z0-9A-Z]{8,20}$',password[0]):
            return JsonResponse({'code': 400, 'errmsg': '密码格式错误'})
        if allow!=True:
            return JsonResponse({'code': 400, 'errmsg': '未勾选协议'})
        if password!=password2:
            return JsonResponse({'code': 400, 'errmsg': '两次密码错误'})
        yzm=get_redis_connection('code')
        print(mobile[0],username[0],password[0])
        yzms=yzm.get(str(mobile[0]))
        print(yzms.decode())
        if yzms.decode()!=sms_code[0]:
            return JsonResponse({'code': 400, 'errmsg': '验证码错误'})
        try:
            user=User.objects.create_user(
                username=username[0],
                password=password[0],
                mobile=mobile[0]
            )
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '注册失败'})
        login(request,user)
        res = JsonResponse({'code': 0, 'errmsg': 'ok'})
        res.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        return res
class logins(View):
    def post(self,request):
        res=json.loads(request.body)
        username=res.get('username')
        password=res.get('password')
        remembered=res.get('remember')
        if not all([username,password]):
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})
        if not re.match(r'1[3-9]\d{9}',username):
            User.USERNAME_FIELD='username'
        else:
            User.USERNAME_FIELD ='mobile'
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '用户名或密码错误'})
        if remembered==True:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)
        login(request,user)
        from goods.utils import catr_login
        res=catr_login(request,user)
        return res
class logouts(View):
    def delete(self,request):
        logout(request)
        res=JsonResponse({'code': 0, 'errmsg': 'ok'})
        res.delete_cookie('username')
        return res
from utils.views import LoginRequiredMixin_2
class info(LoginRequiredMixin_2,View):
    def get(self,request):
        try:
            user=User.objects.get(id=request.user.id)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '失败'})
        info_data={
            'username':user.username,
            'mobile':user.mobile,
            'email':user.email,
            'email_active':user.email_active
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok','info_data':info_data})
from django.conf import settings
from django.core.mail import send_mail
from .utils import jiemi,jiami
class emails(LoginRequiredMixin_2,View):
    def put(self,request):
        email=json.loads(request.body).get('email')
        if not re.match('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',email):
            return JsonResponse({'code': 400, 'errmsg': '邮箱格式错误'})
        try:
            user=User.objects.get(id=request.user.id)
            user.email=email
            user.save()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '失败'})
        id=request.user.id
        tocker=jiami(id)
        subject = '图灵商城验证'  # 主题
        message = ''  # 内容
        sender = settings.EMAIL_FROM  # 发送邮箱，已经在settings.py设置，直接导入
        receiver = [email]  # 目标邮箱 切记此处只能是列表或元祖
        html_message ='<p>尊敬的用户您好！</p>' \
                      '<p>感谢您使用图灵商城。</p>' \
                      '<a href=http://127.0.0.1:8080/success_verify_email.html?tocker=%s>激活链接地址</a>' % tocker  # 发送html格式
        print(html_message)
        from celery_tasks.email.tasks import send_mails
        send_mails(subject, message, sender, receiver, html_message)
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
from .models import Address
class emails_verification(View):
    def put(self,request):
        tocker=request.GET.get('tocker')
        if tocker==None:
            return JsonResponse({'code': 400, 'errmsg': '验证错误'})
        id=jiemi(tocker)
        if id==None:
            return JsonResponse({'code': 400, 'errmsg': '验证错误'})
        print(id)
        user=User.objects.get(id=id)
        user.email_active='True'
        user.save()
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
class addresses_create(LoginRequiredMixin_2,View):
    def post(self,request):
        res=json.loads(request.body)
        receiver=res.get('receiver')
        province_id=res.get('province_id')
        city_id=res.get('city_id')
        district_id=res.get('district_id')
        place=res.get('place')
        mobile=res.get('mobile')
        tel=res.get('tel')
        email=res.get('email')
        user=request.user
        if not all([receiver,province_id,city_id,district_id,province_id,mobile]):
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})
        if not re.match(r'1[3-9]\d{9}',mobile):
            return JsonResponse({'code': 400, 'errmsg': '电话格式错误'})
        try:
            print(user,receiver,place,province_id,city_id,district_id,mobiles)
            i=Address.objects.create(
                user=request.user,
                title=place,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '添加失败'})
        address={
            'id': i.id,
            'title': i.title,
            'receiver': i.receiver,
            'place': i.place,
            'province': i.province.name,
            'city': i.city.name,
            'district': i.district.name,
            'mobile': i.mobile,
            'tel': i.tel,
            'email': i.email
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok','address':address})
class addresses(LoginRequiredMixin_2,View):
    def get(self,request):
        user=request.user
        address=Address.objects.filter(user_id=user,is_deleted=False)
        addresse=[]
        for i in address:
            addresse.append({
                'id':i.id,
                'title': i.title,
                'receiver':i.receiver,
                'place':i.place,
                'province':i.province.name,
                'city':i.city.name,
                'district':i.district.name,
                'mobile':i.mobile,
                'tel':i.tel,
                'email':i.email
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok','addresses':addresse})
class addresses_id(LoginRequiredMixin_2,View):
    def put(self,request,id):
        res = json.loads(request.body)
        receiver = res.get('receiver')
        province_id = res.get('province_id')
        city_id = res.get('city_id')
        district_id = res.get('district_id')
        place = res.get('place')
        mobile = res.get('mobile')
        tel = res.get('tel')
        email = res.get('email')
        user = request.user
        if not all([receiver, province_id, city_id, district_id, province_id, mobile]):
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})
        if not re.match(r'1[3-9]\d{9}', mobile):
            return JsonResponse({'code': 400, 'errmsg': '电话格式错误'})
        try:
            print(user, receiver, place, province_id, city_id, district_id, mobile)
            ii = Address.objects.filter(id=id).update(
                title=place,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '修改失败'})
        address=Address.objects.get(id=id)
        print(address.receiver)
        address = {
            'id': id,
            'title': address.receiver,
            'receiver': address.receiver,
            'place': address.place,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'mobile': address.mobile,
            'tel': address.tel,
            'email': address.email
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok','address':address})
    def delete(self,request,id):
        try:
            Address.objects.filter(id=id).update(is_deleted=True)
        except:
            return JsonResponse({'code': 400, 'errmsg': '删除失败'})
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
from django.contrib.auth.hashers import check_password
class password(LoginRequiredMixin_2,View):
    def put(self,request):
        res=json.loads(request.body)
        old_password=res.get('old_password')
        new_password=res.get('new_password')
        new_password2=res.get('new_password2')
        if not  all([old_password,new_password,new_password2]):
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})
        if new_password!=new_password2:
            return JsonResponse({'code': 400, 'errmsg': '两次密码不对等'})
        user=User.objects.get(id=request.user.id)
        pwd_bool = user.check_password(old_password)
        if not pwd_bool:
            return JsonResponse({'code': 400, 'errmsg': '旧密码错误'})
        user.set_password(new_password)
        user.save()
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
from goods.models import SKU
class browse_histories(LoginRequiredMixin_2,View):
    def post(self,request):
        sku_id=json.loads(request.body).get('sku_id')
        res=get_redis_connection('histories')
        res.lpush(request.user.id,sku_id)
        res.ltrim(request.user.id,0,4)
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
    def get(self, request):
        res = get_redis_connection('histories')
        skus=res.lrange(request.user.id,0,4)
        lists=[]
        for sku in skus:
            cat=SKU.objects.get(id=sku.decode())
            lists.append({
                'price':cat.price,
                'name':cat.name,
                'id':cat.id,
                'default_image_url':cat.default_image.url
            })
        print(lists)
        return JsonResponse({'code': 0, 'errmsg': 'ok','skus':lists})