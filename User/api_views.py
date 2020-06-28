from SmartDjango import Analyse, ModelError, E
from django.views import View
from smartify import P
from Base.auth import Auth
from Base.geetests import Geetest
from Base.send_mobile import SendMobile
from User.models import User, UserP


class UserView(View):
    @staticmethod
    @Auth.require_login
    def get(request):
        """ GET /api/user/

        获取我的信息
        """
        user = request.user
        # print(user.username)
        return UsernameView.get_info(user.username)

    @staticmethod
    @Analyse.r(b=[UserP.username, UserP.password, UserP.nickname, P('code', '验证码')])
    def post(request):
        """ POST /api/user/

        创建用户
        """
        phone = SendMobile.check_captcha(request, **request.d.dict('code'))
        user = User.create(phone, **request.d.dict('username', 'password', 'nickname'))
        return Auth.get_login_token(user)

    @staticmethod
    @Analyse.r(b={
        UserP.password.clone().default(None),
        UserP.password.clone().rename('old_password').default(None),
        P('nickname', '昵称').default(None)  # 教学示范
    })
    @Auth.require_login
    def put(request):
        """ PUT /api/user/

        修改用户信息
        """
        user = request.user

        password = request.d.password
        nickname = request.d.nickname
        old_password = request.d.old_password

        if password is not None:
            user.change_password(password, old_password)
        else:
            user.modify_info(nickname)
        return user.d()


class UsernameView(View):
    @staticmethod
    @Analyse.r(a=[UserP.username])
    def get(request):
        """ GET /api/user/@:username

        获取用户信息
        """
        username = request.d.username
        # print(username)
        user = User.get_user_by_username(username)
        return user.d()

    @staticmethod
    def get_info(username):
        print(username)
        user = User.get_user_by_username(username)
        return user.d()

    @staticmethod
    @Analyse.r(a=[UserP.username])
    # @Auth.require_root
    def delete(request):
        """ DELETE /api/user/@:username

        删除用户
        """
        username = request.d.username
        user = User.get_user_by_username(username)
        user.delete()


class TokenView(View):
    @staticmethod
    @Analyse.r(b=[P('geetest_challenge', 'challenge'), P('geetest_seccode', 'seccode'), P('geetest_validate', '验证码'),
                  UserP.username, UserP.password])
    @Auth.geetestValidate
    def post(request):
        """ POST /api/user/token

        登录获取token
        """
        user = User.authenticate(request.d.username, request.d.password)
        return Auth.get_login_token(user)


class SendRegisterCaptchaView(View):
    @staticmethod
    # P('challenge', '极验深知凭证'),
    @Analyse.r(b=[P('geetest_challenge', 'challenge'), P('geetest_seccode', 'seccode'), P('geetest_validate', '验证码'), P('phone', '手机号')])
    @Auth.geetestValidate
    def post(request):
        """
        POST /api/user/registerCaptcha
        :param request:
                code: 短信验证码
                phone: 手机号
        :return:
        """
        phone = request.d.phone

        try:
            User.get_by_phone(phone)
            SendMobile.send_captcha(request, phone)
            toast_msg = '验证码已发送，请查收'
            send = True
        except E:
            toast_msg = '手机号已注册'
            send = False
        return dict(
            send=send,
            toast_msg=toast_msg
        )
