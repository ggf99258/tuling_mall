import pickle,base64
from django_redis import get_redis_connection
from django.http import JsonResponse
def catr_login(request,user):
    res = request.COOKIES.get('cart')
    if res:
        cart_olds = pickle.loads(base64.b64decode(res.encode()))
        for cart in cart_olds.keys():
            print(cart)
            code=get_redis_connection('cart')
            code.hset('cart_%s' % user.id,cart,cart_olds[cart]['count'])
            code.sadd('selected_%s' % user.id,cart)
    res = JsonResponse({'code': 0, 'errmsg': 'ok'})
    res.delete_cookie('cart')
    res.set_cookie('username', user.username, max_age=3600 * 24 * 15)
    return res