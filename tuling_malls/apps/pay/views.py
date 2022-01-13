from django.shortcuts import render
from django.views import View
from alipay import AliPay,AliPayConfig
# Create your views here.
from .models import Payment
from cart.models import OrderInfo
from tuling_malls import settings
from django.http import JsonResponse
class payment_order_id(View):
    def get(self,request,order_id):
        try:
            order_obj = OrderInfo.objects.get(pk=order_id)
        except:
            raise Exception("订单号无效")
        app_private_key_path=open(settings.ALIPAY_PRIVATE_KEY_PATH).read()
        alipay_public_key_path=open(settings.ALIPAY_PUBLIC_KEY_PATH).read()
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            app_private_key_string=app_private_key_path,
            alipay_public_key_string=alipay_public_key_path,
            sign_type='RSA2',
            debug=settings.ALIPAY_DEBUG,
            config=AliPayConfig(timeout=300)
        )
        order_string = alipay.api_alipay_trade_page_pay(
            subject=settings.ALIPAY_SUBJECT,
            out_trade_no=order_id,  # 订单编号
            total_amount=str(order_obj.total_amount),  # 支付总金额，类型为Decimal(),不支持序列化，需要强转成str
            return_url=settings.ALIPAY_RETURN_URL  # 支付成功后的回调地址
        )
        # 4.返回url
        print(settings.ALIPAY_GATE + order_string)
        return JsonResponse({'code': 0, 'errmsg': 'ok','alipay_url': settings.ALIPAY_GATE + order_string})
class order_string(View):
    def put(self,request):
        data = request.query_params.dict()
        print(data)
        # 2.验证是否支付成功
        # 2.1删除签名,不参与验证
        signature = data.pop("sign")
        app_private_key_path = open(settings.ALIPAY_PRIVATE_KEY_PATH).read()
        alipay_public_key_path = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()
        # 2.2 创建alipay对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            sign_type='RSA2',
            app_private_key_string=app_private_key_path,
            alipay_public_key_string=alipay_public_key_path,
            debug=settings.ALIPAY_DEBUG,
            config=AliPayConfig(timeout=300)
        )
        success = alipay.verify(data, signature)
        if success:
            order_id = data["out_trade_no"]
            # 2 修改订单状态
            try:
                order_obj = OrderInfo.objects.get(pk=order_id)
            except:
                raise Exception("订单号无效")
            order_obj.status = 2
            order_obj.save()
            # 3.创建订单支付对象
            trade_no = data.get('trade_no')  # 获取流水号
            Payment.objects.create(
                order_id=order_id,
                trade_no=trade_no
            )
            return JsonResponse({"trade_id": trade_no,'amount':order_obj.total_amount})
        else:
            raise Exception("支付失败")