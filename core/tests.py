from django.core.management import call_command
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse


class RolesAndDashboardTests(TestCase):
    def test_manager_dashboard_access(self):
        manager_group = Group.objects.create(name='Manager')
        user = User.objects.create_user(username='manager_test', password='Pass12345')
        user.groups.add(manager_group)

        self.client.force_login(user)
        response = self.client.get(reverse('manager_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard Manager')

    def test_seed_roles_command_creates_two_users_per_role(self):
        call_command('seed_roles')

        for role in ['Manager', 'Technician', 'Customer']:
            self.assertEqual(User.objects.filter(groups__name=role).count(), 2)
