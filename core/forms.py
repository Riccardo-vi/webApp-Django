from django import forms
from django.contrib.auth.models import User
from .models import Ticket, Device

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'device', 'priority', 'status', 'technician', 'expected_close_date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user is not None:
            # 1. Se l'utente è Manager, vede TUTTI i dispositivi. Altrimenti solo i suoi.
            if user.groups.filter(name="Manager").exists():
                self.fields['device'].queryset = Device.objects.all()
            else:
                self.fields['device'].queryset = Device.objects.filter(owner=user)

            # 2. Nel menu a tendina dei tecnici, mostra SOLO gli utenti del gruppo "Technician"
            self.fields['technician'].queryset = User.objects.filter(groups__name="Technician")

            # 3. Se l'utente è Customer → rimuovi i campi che NON deve vedere
            if user.groups.filter(name="Customer").exists():
                self.fields.pop('priority', None)
                self.fields.pop('status', None)
                self.fields.pop('technician', None)
                self.fields.pop('expected_close_date', None)