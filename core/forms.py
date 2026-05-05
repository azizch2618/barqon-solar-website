from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm



from .models import Contact

User = get_user_model()


INPUT_CLASS = "app-input"
TEXTAREA_CLASS = "app-textarea"
SELECT_CLASS = "app-select"


class PublicSolarInquiryForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "name",
            "phone",
            "email",
            "subject",
            "property_type",
            "city_area",
            "installation_address",
            "wapda_bill",
            "wapda_bill_2",
            "wapda_bill_3",
            "system_type_preference",
            "monthly_bill",
            "bill_month_1",
            "bill_amount_1",
            "bill_month_2",
            "bill_amount_2",
            "bill_month_3",
            "bill_amount_3",
            "fans",
            "lights",
            "ac",
            "fridge",
            "heater",
            "iron",
            "computers",
            "motors",
            "other_load_watts",
            "load_details",
            "desired_backup_hours",
            "battery_preference",
            "wants_earth_bore",
            "preferred_contact_method",
            "message",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Your full name"}),
            "phone": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "03XX-XXXXXXX"}),
            "email": forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "name@example.com"}),
            "subject": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Home solar planning"}),
            "property_type": forms.Select(attrs={"class": SELECT_CLASS}),
            "city_area": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Multan, Lahore, Bahawalpur..."}),
            "installation_address": forms.Textarea(attrs={"class": TEXTAREA_CLASS, "rows": 3, "placeholder": "Street, colony, landmark"}),
            "wapda_bill": forms.FileInput(attrs={"class": INPUT_CLASS, "accept": ".pdf,image/*", "data-bill-file": "1"}),
            "wapda_bill_2": forms.FileInput(attrs={"class": INPUT_CLASS, "accept": ".pdf,image/*", "data-bill-file": "2"}),
            "wapda_bill_3": forms.FileInput(attrs={"class": INPUT_CLASS, "accept": ".pdf,image/*", "data-bill-file": "3"}),
            "system_type_preference": forms.Select(attrs={"class": SELECT_CLASS}),
            "monthly_bill": forms.NumberInput(attrs={"class": INPUT_CLASS, "placeholder": "25000"}),
            "bill_month_1": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Month 1 (e.g. Jan)"}),
            "bill_amount_1": forms.NumberInput(attrs={"class": INPUT_CLASS, "placeholder": "Amount"}),
            "bill_month_2": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Month 2 (e.g. Feb)"}),
            "bill_amount_2": forms.NumberInput(attrs={"class": INPUT_CLASS, "placeholder": "Amount"}),
            "bill_month_3": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Month 3 (e.g. Mar)"}),
            "bill_amount_3": forms.NumberInput(attrs={"class": INPUT_CLASS, "placeholder": "Amount"}),
            "fans": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 0}),
            "lights": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 0}),
            "ac": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 0}),
            "fridge": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 0}),
            "heater": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 0}),
            "iron": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 0}),
            "computers": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 0}),
            "motors": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 0}),
            "other_load_watts": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 0, "placeholder": "Other load in watts"}),
            "load_details": forms.Textarea(attrs={"class": TEXTAREA_CLASS, "rows": 4, "placeholder": "Water pump, microwave, washing machine, freezer..."}),
            "desired_backup_hours": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 0, "step": "0.5"}),
            "battery_preference": forms.Select(attrs={"class": SELECT_CLASS}),
            "preferred_contact_method": forms.Select(attrs={"class": SELECT_CLASS}),
            "message": forms.Textarea(attrs={"class": TEXTAREA_CLASS, "rows": 4, "placeholder": "Tell us what you want to run and what matters most to you."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["wants_earth_bore"].widget.attrs.update({"class": "app-checkbox"})
        
        # Make fields optional to allow partial form completion in multi-step flow
        optional_fields = [
            "email", "subject", "property_type", "city_area", "installation_address",
            "wapda_bill", "wapda_bill_2", "wapda_bill_3",
            "system_type_preference", "monthly_bill", 
            "bill_month_1", "bill_amount_1", 
            "bill_month_2", "bill_amount_2", 
            "bill_month_3", "bill_amount_3",
            "fans", "lights", "ac", "fridge", "heater", "iron", "computers", "motors",
            "other_load_watts", "load_details", "desired_backup_hours", 
            "battery_preference", "preferred_contact_method", "message"
        ]
        for field_name in optional_fields:
            if field_name in self.fields:
                self.fields[field_name].required = False


class UnifiedLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Enter your email or username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "placeholder": "••••••••"})
    )


class UnifiedRegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Full Name"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "name@example.com"})
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "03XX-XXXXXXX"})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "full_name", "email", "phone")
        widgets = {
            "username": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Choose a username"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": INPUT_CLASS, "placeholder": "Create password"})
        self.fields["password2"].widget.attrs.update({"class": INPUT_CLASS, "placeholder": "Confirm password"})

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get("full_name", "")
        if " " in full_name:
            user.first_name, user.last_name = full_name.split(" ", 1)
        else:
            user.first_name = full_name
        user.email = self.cleaned_data.get("email")
        user.phone = self.cleaned_data.get("phone")
        if commit:
            user.save()
        return user


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "name@example.com"}),
        }



