from django.contrib import admin
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _

from ip_assembler.forms import IPBatchMergeForm
from ip_assembler.models import IP


class IPAdmin(admin.ModelAdmin):
    ordering = ['seg_0', 'seg_1', 'seg_2', 'seg_3', ]

    def get_urls(self):
        """
        Returns the urls for the model.
        """
        urls = super(IPAdmin, self).get_urls()
        my_urls = patterns(
            '',
            url(r'^batch_process_ips/$', self.admin_site.admin_view(self.batch_process_ips_view), name='batch_process_ips_view')
        )
        return my_urls + urls

    def batch_process_ips_view(self, request):
        info_text = _('No errors')

        if request.method == 'POST':
            form = IPBatchMergeForm(request.POST)
            if form.is_valid():
                # add IPs

                def filter_ips(ip):
                    return len(ip) > 0

                ips = filter(filter_ips, form.cleaned_data['ips'].split('\r\n'))
                ip_count_before = IP.objects.count()
                merged_ip_count = 0

                if len(ips) > 0:
                    ips_created = 0
                    # for each ip, check if already existent, if not add
                    for ip in ips:
                        (s0, s1, s2, s3) = ip.split('.')
                        (ip_db, is_ip_created) = IP.objects.get_or_create(seg_0=s0, seg_1=s1, seg_2=s2, seg_3=s3, )
                        if is_ip_created:
                            ips_created += 1

                    # display an info
                    info_text = _('%(ip_count)d IPs were given,<br /> %(ips_created)d IPs were created' % {'ip_count': len(ips), 'ips_created': ips_created})

                # unify them
                clean_ips = form.cleaned_data['show_cleaned_list']
                if clean_ips:
                    # store the ips that have already been processed
                    processed_ips = []

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

                    info_text += ',<br /> ' + _('%(merged_ip_count)d IPs merged' % {'merged_ip_count': merged_ip_count})
                    info_text += ',<br /> ' + _('%(ip_count_before)d IPs before' % {'ip_count_before': ip_count_before})
                    info_text += ',<br /> ' + _('%(ip_count_after)d IPs after' % {'ip_count_after': IP.objects.count()})

        else:
            form = IPBatchMergeForm()

        return render(
            request,
            'admin/batch_process_ips.html',
            {
                'form': form,
                'info_text': info_text,
                # PostgreSQL specific!
                'ips': IP.objects.extra(
                    select={'seg0': 'seg_0::int', 'seg1': 'seg_1::int', 'seg2': 'seg_2::int'},
                    order_by=['seg0', 'seg1', 'seg2', 'seg_3']
                )
            }
        )

admin.site.register(IP, IPAdmin)
