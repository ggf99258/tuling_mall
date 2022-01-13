from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
class LoginRequiredMixin_2(LoginRequiredMixin):
    def handle_no_permission(self):
        return JsonResponse({'code':400,'errmsg':'未登录'})