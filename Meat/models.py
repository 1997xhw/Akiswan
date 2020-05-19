from SmartDjango import models, E
import datetime

from smartify import P

from Base.pager import target_timer


@E.register()
class MeatError:
    CREATE_MEAT = E("创建MEAT错误")
    GET_MEAT_BY_PK = E("获取MEAT错误")
    CHANGE_MEAT_STATUS = E("改变STATUS失败")
    CHANGE_MEAT_ACHIEVE = E("改变ACHIEVE失败")


class Meat(models.Model):
    """
    肉类（任务）
    """
    # 天鹅肉
    content = models.TextField(
        default=None,
        null=True,
    )
    # 天鹅肉所有者
    toad = models.ForeignKey(
        'User.User',
        related_name='toad_user',
        on_delete=models.CASCADE,
    )
    # 目标时间
    target_time = models.DateTimeField(
        null=True
    )
    # 创建时间
    create_time = models.DateTimeField(
        auto_now_add=True

    )
    # 肉质及状态
    # 0还没熟
    # 1熟了（已到时间）
    # 2吃上了
    # 3下次一定
    status = models.IntegerField(
        default=0
    )
    # 短信提醒开关
    notification = models.BooleanField(
        # 是否开启短信提醒功能
        default=False
    )
    # 标记
    achieve = models.BooleanField(
        default=False
    )

    @classmethod
    def create(cls, user, content, target_time, notification):
        print("create++++++++++++++++")
        try:
            meat = cls(
                content=content,
                toad=user,
                target_time=target_time,
                create_time=datetime.datetime.now(),
                status=0,
                notification=notification,
                achieve=False
            )
            meat.save()
            user.add_meat_quantity()
        except Exception as err:
            raise MeatError.CREATE_MEAT(debug_message=err)
        return meat

    @classmethod
    def change_meat_status(cls, meat, status):
        try:
            meat.status = status
            meat.save()
        except Exception:
            raise MeatError.CHANGE_MEAT_STATUS
        if not meat.achieve and status > 1:
            cls.change_meat_achieve(meat, True)
        return meat

    @staticmethod
    def change_meat_achieve(meat, achieve):
        try:
            meat.achieve = achieve
            meat.save()
        except Exception:
            raise MeatError.CHANGE_MEAT_ACHIEVE
        meat.toad.reduce_meat_quantity()

    @classmethod
    def get_meat_by_pk(cls, tid):
        try:
            return cls.objects.get(pk=tid)
        except Exception:
            raise MeatError.GET_MEAT_BY_PK

    @classmethod
    def get_meat_list(cls, user):
        pass

    def d(self):
        return self.dictor('pk->mid', 'content', 'toad', 'target_time', 'create_time', 'status', 'notification',
                           'achieve')

    def d_meat_list(self):
        return self.dictor('pk->mid', 'content', 'status', 'achieve')

    def _readable_toad(self):
        if self.toad:
            return self.toad.d()

    def _readable_target_time(self):
        return self.target_time.timestamp()

    def _readable_create_time(self):
        return self.create_time.timestamp()


class MeatP:
    content, status = Meat.get_params('content', 'status')
    notification = P('notification', '目标日期').default(False).process(bool)
    target_time = P('target_time', '目标时间').process(int).process(target_timer)
    mid = P('mid', '天鹅肉id', 'meat').process(int).process(Meat.get_meat_by_pk)
