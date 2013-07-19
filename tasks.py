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
    run_every = timedelta(minutes=30)

    def run(self, **kwargs):
        """
        Checks the IMAP mailbox for new mails and tries to handle them.
        """
        try:
            # connect to server and login
            mail = imaplib.IMAP4_SSL(settings.IMAP_SERVER)
            mail.login(settings.IMAP_USERNAME, settings.IMAP_PASSWORD)
            mail.select()

            # search for all mails in the mailbox
            result, mail_indices = mail.search(None, 'ALL')

            # if everything was ok...
            if result == 'OK':

                # if there is mail, set the regex expressions
                if len(mail_indices[0].split()) > 0:
                    self.regex_expressions = [
                        re.compile(".*ip_tracer/(.*)\).*", re.IGNORECASE | re.MULTILINE | re.UNICODE | re.VERBOSE),
                        re.compile(".*IP address (.*) has been.*")
                    ]

                # iterate the mail indices and fetch the mails
                for mail_index in mail_indices[0].split():
                    # mail data is a list with a tuple
                    sub_result, mail_data = mail.fetch(mail_index, '(BODY[TEXT])')
                    if sub_result == 'OK':

                        # fetch the ips
                        ips = list_remove_duplicates(
                            self.find_ips(''.join(mail_data[0]))
                        )

                        # if ips found, add them and delete the mail
                        if len(ips) > 0:
                            IP.batch_add_ips(ips)

                    else:
                        logger.error('fetching mail with index %(index)d failed' % {'index': mail_index})

            else:
                logger.error('search returned not OK')

            mail.close()
            mail.logout()
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
