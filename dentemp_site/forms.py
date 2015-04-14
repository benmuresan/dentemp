from django import forms
from .models import UserProfile, OfficeProfile
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit


class NewUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout("first_name", "last_name", "email", )
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)

    class Meta:
        model = UserProfile


class NewOfficeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewOfficeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout("auth_user", "office_name", "email", "address", "has_hired", )
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)

    class Meta:
        model = OfficeProfile