from django.core.management.base import BaseCommand, CommandError

from ip_assembler.tasks import IPEMailChecker


class Command(BaseCommand):
    """
    Helper command for testing several functionality.
    """

    def handle(self, *args, **options):
        commands = {
            'email_checker_task': {
                'help': 'Runs the IPEMailChecker task.',
                'method': self.email_checker_task,
            },
        }

        if len(args) == 0:
            raise CommandError(
                'Please specify a subcommand to run. This can be:\n' + '\n'.join(
                    ['\t%(key)s:\t%(help)s' % {'key': key, 'help': value['help']} for key, value in commands.items()]
                )
            )

        # run the appropriate subcommand
        commands[args[0]]['method']()

    def email_checker_task(self):
        """
        Executes the IPEMailChecker tasks (that is a periodic task!)
        """
        IPEMailChecker().delay()
