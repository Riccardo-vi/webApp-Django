from django import forms
from .models import Ticket, Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['brand', 'model', 'serial_number']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'device', 'priority', 'status', 'technician', 'expected_close_date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Se l'utente è Customer → rimuovi i campi che NON deve vedere
        if user and user.groups.filter(name="Customer").exists():
            self.fields.pop('priority')
            self.fields.pop('status')
            self.fields.pop('technician')
            self.fields.pop('expected_close_date')