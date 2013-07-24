import logging
import imaplib
import re

from .models import IP

from celery.task import PeriodicTask

from datetime import timedelta

from django.conf import settings

from shared.utils import list_remove_duplicates


logger = logging.getLogger('ip_assembler')


class IPEMailChecker(PeriodicTask):
    """
    Periodic task checking the mailbox for new mails about WP spamming..
    """
    run_every = timedelta(minutes=120)

    def run(self, **kwargs):
        """
        Checks the IMAP mailbox for new mails and tries to handle them.
        """
        try:
            # connect to server and login
            box = imaplib.IMAP4_SSL(settings.IMAP_SERVER)
            box.login(settings.IMAP_USERNAME, settings.IMAP_PASSWORD)
            box.select()

            # search for all mails in the mailbox
            result, mail_indices = box.search(None, 'ALL')

            # if everything was ok...
            if result == 'OK':

                # check number of mails
                mail_count = len(mail_indices[0].split())
                logger.info('found %(mail_count)d mails...' % {'mail_count': mail_count})

                # if there is mail, set the regex expressions
                if mail_count > 0:
                    self.regex_expressions = [
                        re.compile(".*ip_tracer/(.*)\).*", re.IGNORECASE | re.MULTILINE | re.UNICODE | re.VERBOSE),
                        re.compile(".*IP address (.*) has been.*")
                    ]

                # iterate the mail indices and fetch the mails
                ips_created = 0
                for mail_index in mail_indices[0].split():
                    logger.info('fetching mail %(mail_index)d...' % {'mail_index': mail_index})
                    # mail data is a list with a tuple
                    sub_result, mail_data = box.fetch(mail_index, '(BODY[TEXT])')
                    if sub_result == 'OK':

                        # fetch the ips
                        ips = list_remove_duplicates(
                            self.find_ips(''.join(mail_data[0]))
                        )

                        # if ips found, add them and delete the mail
                        if len(ips) > 0:
                            logger.info('found %(count)d IPs' % {'count': len(ips)})
                            ips_created += IP.batch_add_ips(ips)
                            box.store(mail_index, '+FLAGS', '\\Deleted')

                    else:
                        logger.error('fetching mail with index %(index)d failed' % {'index': mail_index})

                # finally, if ips were added, unify the IPs
                if ips_created > 0:
                    logger.info('created %(count)d IPs' % {'count': ips_created})
                    IP.unify_ips()

            else:
                logger.error('search returned not OK')

            box.close()
            box.logout()
        except:
            logger.exception('retrieving mail failed')

    def find_ips(self, text):
        """
        Uses some regex to find IPs within the text.
        :param text: the text to search in
        :type text: str
        :return: list of ips
        :rtype: list
        """
        for regex in self.regex_expressions:
            ips = regex.findall(text)
            if len(ips) > 0:
                return ips
        return []
