from bootstrap import admin_actions_registry

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _, ugettext_lazy

# admin action to be displayed in action row
admin_actions_registry['ip_assembler'] = lambda: \
    '<a href="%s" class="button">IP Batch Processing</a>' % reverse('admin:batch_process_ips_view')


class IP(models.Model):
    seg_0 = models.CharField(max_length=3, verbose_name=_('Segment 1'))
    seg_1 = models.CharField(max_length=3, verbose_name=_('Segment 2'))
    seg_2 = models.CharField(max_length=3, verbose_name=_('Segment 3'))
    seg_3 = models.CharField(max_length=3, verbose_name=_('Segment 4'))

    def __unicode__(self):
        return u'%s.%s.%s.%s' % (self.seg_0, self.seg_1, self.seg_2, self.seg_3)

    class Meta:
        app_label = 'ip_assembler'
        verbose_name = ugettext_lazy('IP')
        verbose_name_plural = ugettext_lazy('IPs')