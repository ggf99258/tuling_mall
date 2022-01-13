from django.shortcuts import render
import pickle,base64
from django.views import View
# Create your views here.
from django.http import JsonResponse
from django_redis import get_redis_connection
import json
from goods.models import SKU
class carts(View):
    def post(self,request):
        res=json.loads(request.body)
        sku_id=res.get('sku_id')
        count=res.get('count')
        user=request.user
        if user.is_authenticated:
            code=get_redis_connection('cart')
            cart=code.hexists('cart_%s'%user.id,sku_id)
            if cart:
                count_old=code.hget('cart_%s'%user.id,sku_id).decode()
                count+=int(count_old)
                code.hset('cart_%s' % user.id, sku_id, count)
            code.hset('cart_%s'%user.id,sku_id,count)
            code.sadd('selected_%s'%user.id,sku_id)
            return JsonResponse({'code': 0, 'errmsg': 'ok'})
        else:
            res=request.COOKIES.get('cart')

            if res:
                cart=pickle.loads(base64.b64decode(res.encode()))
                if sku_id in cart:
                    count+=cart[sku_id]['count']
                cart[sku_id]={'count':count,'selected':True}
            else:
                cart= {}
                cart[sku_id] = {'count': count, 'selected': True}
            cats=base64.b64encode(pickle.dumps(cart)).decode()
            ress=JsonResponse({'code': 0, 'errmsg': 'ok'})
            ress.set_cookie('cart',cats)
            return ress
    def get(self,request):
        user = request.user
        if user.is_authenticated:
            code = get_redis_connection('cart').hgetall('cart_%s'%user.id)
            selection=get_redis_connection('cart').smembers('selected_%s'%user.id)
            cart_skus=[]
            for sku,counts in code.items():
                sku_id=sku.decode()
                count=counts.decode()
                skus=SKU.objects.get(id=sku_id)
                if sku_id.encode() in selection:
                    selections=True
                else:
                    selections =False
                cart_skus.append({
                        'id':sku_id,
                        'count':int(count),
                        'price':skus.price,
                        'name':skus.name,
                        'default_image_url': skus.default_image.url,
                        'selected':selections
                    })
            return JsonResponse({'code': 0, 'errmsg': 'ok','cart_skus':cart_skus})
        else:
            res = request.COOKIES.get('cart')
            cart_skus = []
            if res:
                cart_olds = pickle.loads(base64.b64decode(res.encode()))
                for i in cart_olds.keys():
                    counts=cart_olds[i]
                    count=counts['count']
                    selected=counts['selected']
                    skus = SKU.objects.get(id=i)
                    cart_skus.append({
                        'id': i,
                        'count': int(count),
                        'price': skus.price,
                        'name': skus.name,
                        'default_image_url': skus.default_image.url,
                        'selected': selected
                    })
                return JsonResponse({'code': 0, 'errmsg': 'ok', 'cart_skus': cart_skus})
    def put(self,request):
        res=json.loads(request.body)
        # print(res)
        sku_id=res.get('sku_id')
        count=res.get('count')
        selected=res.get('selected')
        user = request.user
        if user.is_authenticated:
            code = get_redis_connection('cart').hset('cart_%s' % user.id,sku_id,count)
            selection = get_redis_connection('cart')
            if selected==True:
                selection.sadd('selected_%s' % user.id,sku_id)
            else:
                selection.srem('selected_%s' % user.id, sku_id)
            return JsonResponse({'code': 0, 'errmsg': 'ok'})
        else:
            res = request.COOKIES.get('cart')
            cart_skus = []
            if res:
                cart_olds = pickle.loads(base64.b64decode(res.encode()))
                cart_olds[sku_id]['count']=count
                # print(cart_olds[sku_id]['selected'])
                if selected == True:
                    cart_olds[sku_id]['selected']=True
                else:
                    cart_olds[sku_id]['selected']=False
                cats = base64.b64encode(pickle.dumps(cart_olds)).decode()
                ress = JsonResponse({'code': 0, 'errmsg': 'ok'})
                ress.set_cookie('cart', cats)
                return ress
    def delete(self,request):
        res = json.loads(request.body)
        sku_id = res.get('sku_id')
        user = request.user
        if user.is_authenticated:
            code = get_redis_connection('cart').hdel('cart_%s' % user.id, sku_id)
            selection = get_redis_connection('cart').srem('selected_%s' % user.id,sku_id)
            return JsonResponse({'code': 0, 'errmsg': 'ok'})
        else:
            res = request.COOKIES.get('cart')
            cart_skus = []
            if res:
                cart_olds = pickle.loads(base64.b64decode(res.encode()))
                cart_olds.pop(sku_id)
                cats = base64.b64encode(pickle.dumps(cart_olds)).decode()
                ress = JsonResponse({'code': 0, 'errmsg': 'ok'})
                ress.set_cookie('cart', cats)
                return ress
class carts_selection(View):
    def put(self,request):
        selected=json.loads(request.body).get('selected')
        user = request.user
        if user.is_authenticated:
            code = get_redis_connection('cart').hkeys('cart_%s' % user.id)
            for i in code:
                if selected == True:
                    code = get_redis_connection('cart').sadd('selected_%s' % user.id,i.decode())
                else:
                    code = get_redis_connection('cart').srem('selected_%s' % user.id, i.decode())
            return JsonResponse({'code': 0, 'errmsg': 'ok'})
        else:
            res = request.COOKIES.get('cart')
            cart_skus = []
            if res:
                cart_olds = pickle.loads(base64.b64decode(res.encode()))
                for sku_id in cart_olds.keys():
                    if selected == True:
                        cart_olds[sku_id]['selected']=True
                    else:
                        cart_olds[sku_id]['selected'] = False
                cats = base64.b64encode(pickle.dumps(cart_olds)).decode()
                ress = JsonResponse({'code': 0, 'errmsg': 'ok'})
                ress.set_cookie('cart', cats)
                return ress
class carts_simple(View):
    def get(self,request):
        user = request.user
        if user.is_authenticated:
            code = get_redis_connection('cart').hgetall('cart_%s' % user.id)
            selection = get_redis_connection('cart').smembers('selected_%s' % user.id)
            cart_skus = []
            for sku, counts in code.items():
                print(sku, counts)
                # for sku,counts in i.items():
                sku_id = sku.decode()
                count = counts.decode()
                print(sku_id, count)
                skus = SKU.objects.get(id=sku_id)
                print(sku_id.encode())
                if sku_id.encode() in selection:
                    selections = True
                else:
                    selections = False
                cart_skus.append({
                    'id': sku_id,
                    'count': int(count),
                    'price': skus.price,
                    'name': skus.name,
                    'default_image_url': skus.default_image.url,
                    'selected': selections
                })
            return JsonResponse({'code': 0, 'errmsg': 'ok', 'cart_skus': cart_skus})
        else:
            res = request.COOKIES.get('cart')
            cart_skus = []
            if res:
                cart_olds = pickle.loads(base64.b64decode(res.encode()))
                for i in cart_olds.keys():
                    counts = cart_olds[i]
                    count = counts['count']
                    selected = counts['selected']
                    skus = SKU.objects.get(id=i)
                    cart_skus.append({
                        'id': i,
                        'count': int(count),
                        'price': skus.price,
                        'name': skus.name,
                        'default_image_url': skus.default_image.url,
                        'selected': selected
                    })
                return JsonResponse({'code': 0, 'errmsg': 'ok', 'cart_skus': cart_skus})
from user.models import Address
class orders_settlement(View):
    def get(self,request):
        user=request.user
        addres=Address.objects.filter(user=user)
        addresses=[]
        for i in addres:
            addresses.append({
                'id':i.id,
                'province':i.province.name,
                'city': i.city.name,
                'district': i.district.name,
                'place': i.place,
                'receiver': i.receiver,
                'mobile':i.mobile
            })
        code = get_redis_connection('cart').hgetall('cart_%s' % user.id)
        selection = get_redis_connection('cart').smembers('selected_%s' % user.id)
        cart_skus = []
        for sku, counts in code.items():
            sku_id = sku.decode()
            count = counts.decode()
            skus = SKU.objects.get(id=sku_id)
            if sku_id.encode() in selection:
                cart_skus.append({
                    'id': sku_id,
                    'count': int(count),
                    'price': skus.price,
                    'name': skus.name,
                    'default_image_url': skus.default_image.url,
                })
        context={
        'skus' : cart_skus,
        'freight' : int(10),
        'addresses' : addresses
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'context': context})
from .models import OrderInfo,OrderGoods
class orders_commit(View):
    def post(self,request):
        res=json.loads(request.body)
        address_id=res.get('address_id')
        pay_method=res.get('pay_method')
        try:
            Address.objects.get(id=address_id)
        except:
            return JsonResponse({'code': 400, 'errmsg': '地址错误'})
        if pay_method==OrderInfo.PAY_METHODS_ENUM["CASH"]:
            status=OrderInfo.ORDER_STATUS_ENUM["UNSEND"]
        else:
            status = OrderInfo.ORDER_STATUS_ENUM["UNPAID"]
        user=request.user
        from django.utils import timezone
        order_id=timezone.localtime().strftime('%Y%m%d%H%M%S%f') + '%09d' % user.id
        # order_id=timezone.localtime().strftime('%Y%m%d%H%M%S%f')+'%09d'%user.id
        from decimal import Decimal
        freight=Decimal('10.00')
        total_amount=Decimal(0)
        total_count=0
        from django.db import transaction
        with transaction.atomic():
            point=transaction.savepoint()
            orderinfo=OrderInfo.objects.create(
                order_id=order_id,
                status=status,
                address_id=address_id,
                freight=freight,
                user=user,
                total_count=0,
                total_amount=0,
                pay_method=pay_method,
            )
            res=get_redis_connection('cart')
            sku_ids=res.hgetall('cart_%s' % user.id)
            for i,t in sku_ids.items():
                sku_id=i.decode()
                if res.sismember('selected_%s' % user.id,sku_id):
                    count=int(res.hget('cart_%s' % user.id,sku_id).decode())
                    sku=SKU.objects.get(id=sku_id)
                    print(sku_id)
                    if count>sku.stock:
                        transaction.savepoint_rollback(point)
                        return JsonResponse({'code': 400, 'errmsg': '商品数量不足'})
                    import time
                    time.sleep(5)
                    total_count+=count
                    amount=count*sku.price
                    total_amount+=amount
                    stock_new=sku.stock-count
                    sales_new=sku.sales+count
                    result=SKU.objects.filter(id=sku_id).update(sales=sales_new,stock=stock_new)
                    if result==0:
                        transaction.savepoint_rollback(point)
                        return JsonResponse({'code': 400, 'errmsg': '商品数量不足!'})
                    orderinfo.total_amount+=amount
                    orderinfo.total_count+=count
                    OrderGoods.objects.create(
                        order=orderinfo,
                        sku=sku,
                        count=count,
                        price=sku.price,
                    )
                orderinfo.save()
        code=get_redis_connection('cart')
        codes=code.pipeline()
        for i in code.hkeys('cart_%s' % user.id):
            print(i)
            if code.sismember('selected_%s' % user.id,i):
                codes.hdel('cart_%s' % user.id,i.decode())
                codes.srem('selected_%s' % user.id,i.decode())
        codes.execute()
        return JsonResponse({'code': 0, 'errmsg': 'ok','order_id':orderinfo.order_id})