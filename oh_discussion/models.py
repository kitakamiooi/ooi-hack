from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class ONode(MPTTModel):
    parent = TreeForeignKey('self', verbose_name='父节点', null=True, blank=True, related_name='children', db_index=True)
    name = models.CharField('节点名称', max_length=20, unique=True, db_index=True,
                            help_text='不超过20字')
    description = models.CharField('节点描述', max_length=100, unique=True, db_index=True,
                                   help_text='不超过100字')
    create_time = models.DateTimeField('节点创建时间', default=timezone.now)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='节点创建者')
    order = models.IntegerField('节点排列顺序', default=0, help_text='在节点列表中的排列顺序，数字小者排列在前')

    class MPTTMeta:
        order_insertion_by = ['order']

    class Meta:
        verbose_name = '讨论区节点'
        verbose_name_plural = '讨论区节点'

    def __str__(self):
        return self.name


class OTopic(models.Model):
    title = models.CharField('标题', max_length=40, help_text='不超过40字')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者')
    node = models.ForeignKey(ONode, verbose_name='所属节点')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    revise_time = models.DateTimeField('修改时间', auto_now=True)
    is_visible = models.BooleanField('是否可见', default=True)
    clicks = models.PositiveIntegerField('点击次数', default=0)
    content = models.TextField('内容', max_length=50000, help_text='不超过50000字')

    class Meta:
        verbose_name = '讨论区主题'
        verbose_name_plural = '讨论区主题'
        ordering = ['-revise_time', '-pk']

    def get_absolute_url(self):
        return reverse_lazy('discussion-topic', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
