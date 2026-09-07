from django import forms
from .models import ContactInquiry


class ContactInquiryForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ("name", "email", "company", "phone", "service", "message")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@company.com", "autocomplete": "email"}),
            "company": forms.TextInput(attrs={"placeholder": "Company (optional)", "autocomplete": "organization"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone (optional)", "autocomplete": "tel"}),
            "service": forms.Select(attrs={"aria-label": "Area of interest"}),
            "message": forms.Textarea(attrs={"placeholder": "Tell us about your idea or business challenge", "rows": 4}),
        }

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 20:
            raise forms.ValidationError("Please share a little more detail (at least 20 characters).")
        return message
