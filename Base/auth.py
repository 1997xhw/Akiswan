from functools import wraps

from SmartDjango import E, Hc
from geetest import GeetestLib

from Base.geetest_api_views import geetest_id, geetest_key
from Base.jtoken import JWT
from User.models import User


@E.register()
class AuthError:
    REQUIRE_LOGIN = E("需要登录", hc=Hc.Unauthorized)
    TOKEN_MISS_PARAM = E("认证口令缺少参数{0}", hc=Hc.Forbidden)
    REQUIRE_ROOT = E("需要root权限")
    MEAT_QUANTITY = E("用户的任务已达上限", hc=Hc.BadRequest)
    MEAT_OWNER = E("该用户不是meat的拥有者", hc=Hc.BadRequest)
    GEETEST_VALIDATE = E("极验验证错误")

class Auth:
    @staticmethod
    def validate_token(request):
        jwt_str = request.META.get('HTTP_TOKEN')
        if not jwt_str:
            raise AuthError.REQUIRE_LOGIN

        return JWT.decrypt(jwt_str)

    @staticmethod
    def get_login_token(user: User):
        token, _dict = JWT.encrypt(dict(
            user_id=user.pk,
        ))
        _dict['token'] = token
        _dict['user'] = user.d()
        return _dict

    @classmethod
    def _extract_user(cls, r):
        r.user = None

        dict_ = cls.validate_token(r)
        user_id = dict_.get('user_id')
        if not user_id:
            raise AuthError.TOKEN_MISS_PARAM('user_id')

        from User.models import User
        r.user = User.get_user_by_id(user_id)

    @classmethod
    def require_login(cls, func):
        @wraps(func)
        def wrapper(r, *args, **kwargs):
            cls._extract_user(r)
            return func(r, *args, **kwargs)

        return wrapper

    @classmethod
    def require_root(cls, func):
        @wraps(func)
        def wrapper(r, *args, **kwargs):
            cls._extract_user(r)
            if r.user.pk != User.ROOT_ID:
                raise AuthError.REQUIRE_ROOT
            return func(r, *args, **kwargs)

        return wrapper

    @classmethod
    def meat_quantity(cls, func):
        @wraps(func)
        def wrapper(r, *args, **kwargs):
            if r.user.meat_quantity >= 3:
                raise AuthError.MEAT_QUANTITY
            return func(r, *args, **kwargs)
        return wrapper

    @classmethod
    def meat_owner(cls, func):
        @wraps(func)
        def wrapper(r, *args, **kwargs):
            if r.user != r.d.meat.toad:
                raise AuthError.MEAT_OWNER
            return func(r, *args, **kwargs)
        return wrapper

    @classmethod
    def geetestValidate(cls, func):
        @wraps(func)
        def wrapper(r, *args, **kwargs):
            gt = GeetestLib(geetest_id, geetest_key)
            challenge = r.d.geetest_challenge
            validate = r.d.geetest_validate
            seccode = r.d.geetest_seccode
            status = r.session[gt.GT_STATUS_SESSION_KEY]
            user_id = r.session["user_id"]
            if status:
                result = gt.success_validate(challenge, validate, seccode, user_id)
            else:
                result = gt.failback_validate(challenge, validate, seccode)
            if result:
                return func(r, *args, **kwargs)
            else:
                raise AuthError.GEETEST_VALIDATE
        return wrapper
