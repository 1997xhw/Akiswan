from SmartDjango import Analyse
from django.views import View
from Base.auth import Auth
from Meat.models import MeatP, Meat


class MeatPoolView(View):
    @staticmethod
    # @Auth.require_login
    def get(request):
        """
        GET /api/meat/pool
        """
        return Meat.objects.all().order_by('-create_time').dict(Meat.d_meat_list)


class MeatView(View):
    @staticmethod
    @Auth.require_login
    def get(request):
        """
        GET /api/meat/
        """
        return Meat.objects.filter(toad=request.user).order_by('-create_time').dict(Meat.d_meat_list)


class MeatStatusView(View):
    @staticmethod
    @Auth.require_login
    @Analyse.r(b=[MeatP.mid, MeatP.status])
    @Auth.meat_owner
    def post(request):
        """
        POST /api/meat/status
        :param request:
        mid meat-id
        status meat状态
        :return:
        """
        return Meat.change_meat_status(request.d.meat, request.d.status).d()


class CreateMeatView(View):
    @staticmethod
    @Auth.require_login
    @Auth.meat_quantity
    @Analyse.r(b=[MeatP.content, MeatP.target_time, MeatP.notification])
    def post(request):
        """
        POST /api/meat/create
        :param request:
        content 内容
        target_time 目标时间
        notification 短信提醒开关

        创建一块天鹅肉
        """
        return Meat.create(request.user, **request.d.dict()).d()


class CheckTargetTimeView(View):
    @staticmethod
    def put(request):
        """
        PUT /api/meat/check
        """
        return Meat.check_target_time()
