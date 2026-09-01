from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User


class Command(BaseCommand):
    help = 'Crea i gruppi e gli utenti di test richiesti per il progetto RepairDesk.'

    def handle(self, *args, **options):
        roles = {
            'Manager': ['manager1', 'manager2'],
            'Technician': ['technician1', 'technician2'],
            'Customer': ['customer1', 'customer2'],
        }

        for role_name, usernames in roles.items():
            group, _ = Group.objects.get_or_create(name=role_name)
            for username in usernames:
                user, created = User.objects.get_or_create(username=username)
                if created:
                    user.set_password('Pass12345')
                    user.save()
                if not user.groups.filter(pk=group.pk).exists():
                    user.groups.add(group)

                self.stdout.write(
                    self.style.SUCCESS(f'Utente {username} pronto con ruolo {role_name}.')
                )

        self.stdout.write(self.style.SUCCESS('Seed ruoli completato.'))
