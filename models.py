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

    @staticmethod
    def batch_add_ips(ips):
        """
        Adds the given list of IPs to the database if the IP is not already there.
        :param ips: list of IPs
        :return: number of created IPs
        :type ips: list
        :rtype: int
        """
        ips_created = 0
        if len(ips) > 0:
            # for each ip, check if already existent, if not add
            for ip in ips:
                (s0, s1, s2, s3) = ip.split('.')
                (ip_db, is_ip_created) = IP.objects.get_or_create(seg_0=s0, seg_1=s1, seg_2=s2, seg_3=s3, )
                if is_ip_created:
                    ips_created += 1
        return ips_created

    @staticmethod
    def unify_ips():
        """
        Unifies the currently saved IPs.
        Unification is based on last IP segment.
        So if there are is e.g. 192.168.128.121 and 192.168.128.122 tthey will be merged to 192.168.128.121.
        This is a little aggressive but the spammers are aggressive, too.
        :return: number of merged ips
        :rtype: int
        """
        # TODO this needs performance improvement!
        # store the ips that have already been processed
        processed_ips = []

        # number of merged ips
        merged_ip_count = 0

        # iterate all ips, might take a while ;-)
        for ip in IP.objects.all().order_by('seg_0', 'seg_1', 'seg_2', 'seg_3'):
            # if the ip was processed, skip
            if ip in processed_ips:
                continue

            # get all siblings of the ip
            siblings = IP.objects.filter(seg_0=ip.seg_0, seg_1=ip.seg_1, seg_2=ip.seg_2, )\
                .exclude(pk=ip.pk)\
                .order_by('seg_0', 'seg_1', 'seg_2', 'seg_3')

            # there are siblings, process...
            if siblings.count() > 0:
                # check if there is already a starred IP in siblings
                try:
                    starred_ip = siblings.get(seg_3='*')
                except:
                # no starred ip, create one
                    if ip.seg_3 != '*':
                        starred_ip = IP.objects.create(seg_0=ip.seg_0, seg_1=ip.seg_1, seg_2=ip.seg_2, seg_3='*', )
                    else:
                        starred_ip = ip

                # delete the others
                for sib_ip in siblings.exclude(pk=starred_ip.pk):
                    processed_ips.append(sib_ip)
                    merged_ip_count += 1
                    sib_ip.delete()

            processed_ips.append(ip)

        return merged_ip_count

    def __unicode__(self):
        return u'%s.%s.%s.%s' % (self.seg_0, self.seg_1, self.seg_2, self.seg_3)

    class Meta:
        app_label = 'ip_assembler'
        verbose_name = ugettext_lazy('IP')
        verbose_name_plural = ugettext_lazy('IPs')