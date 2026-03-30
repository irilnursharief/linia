from django import forms
from branches.models import Branch
from services.models import Service
from .models import Ticket


class GetTicketForm(forms.Form):
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.filter(is_active=True),
        empty_label="Select a Branch",
        widget=forms.Select(
            attrs={
                "hx-get": "/ajax/load-services/",
                "hx-target": "#id_service",
                "hx-trigger": "change",
                "hx-include": "[name='branch']",
            }
        ),
    )

    service = forms.ModelChoiceField(
        queryset=Service.objects.none(),
        empty_label="Select a Service",
        widget=forms.Select(attrs={"id": "id_service"}),  # 👈 important for HTMX target
    )

    client_type = forms.ChoiceField(choices=Ticket.ClientType.choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 👇 KEEP THIS (very important for POST validation)
        if "branch" in self.data:
            try:
                branch_id = int(self.data.get("branch"))
                self.fields["service"].queryset = Service.objects.filter(
                    branch_id=branch_id, is_active=True
                )
            except (ValueError, TypeError):
                pass


class PreRegisterForm(forms.Form):
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.filter(is_active=True),
        empty_label="Select a Branch",
        widget=forms.Select(
            attrs={
                "hx-get": "/ajax/load-services/",
                "hx-target": "#id_service_pre",
                "hx-trigger": "change",
                "hx-include": "[name='branch']",
            }
        ),
    )

    service = forms.ModelChoiceField(
        queryset=Service.objects.none(),
        empty_label="Select a Service",
        widget=forms.Select(
            attrs={
                "id": "id_service_pre"  # ← different id to avoid conflict with GetTicketForm
            }
        ),
    )

    client_type = forms.ChoiceField(choices=Ticket.ClientType.choices)

    scheduled_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "branch" in self.data:
            try:
                branch_id = int(self.data.get("branch"))
                self.fields["service"].queryset = Service.objects.filter(
                    branch_id=branch_id, is_active=True
                )
            except (ValueError, TypeError):
                pass
