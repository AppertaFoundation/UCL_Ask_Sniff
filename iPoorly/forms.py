""" forms used in the website. These forms are processed in view.py """
import datetime
from django import forms
from django.forms.widgets import HiddenInput
from redactor.widgets import RedactorEditor
from .models import SubHeading, Heading, Category, DiaryLog

class LoginForm(forms.Form):
    """ login form used in the index view """
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'id':'username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'id':'password'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'required': 'required'})
        self.fields['password'].widget.attrs.update({'required': 'required'})

class SignUpForm(forms.Form):
    """ signup form used in the index view """
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'id':'username2'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'id':'password2'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'id':'email'}))

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'required': 'required'})
        self.fields['password'].widget.attrs.update({'required': 'required'})
        self.fields['email'].widget.attrs.update({'required': 'required'})

class ForgotPassword(forms.Form):
    """ form used for forgot password """
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'id':'username'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'id':'email'}))
    password = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'id':'password'}))

    def __init__(self, *args, **kwargs):
        super(ForgotPassword, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'required': 'required'})
        self.fields['password'].widget.attrs.update({'required': 'required'})
        self.fields['email'].widget.attrs.update({'required': 'required'})

class AddChildForm(forms.Form):
    """ form used to get a childs information """
    childName = forms.CharField(label='Child Name', max_length=100, widget=forms.TextInput(attrs={'id':'childName'}))
    dob = forms.DateField(label='Child Date of Birth', widget=forms.DateInput(attrs={'id':'dob', 'type':'date'}))

    def __init__(self, *args, **kwargs):
        super(AddChildForm, self).__init__(*args, **kwargs)
        self.fields['childName'].widget.attrs.update({'required': 'required'})
        self.fields['dob'].widget.attrs.update({'required': 'required', 'max':str(datetime.datetime.today().strftime('%Y-%m-%d'))})
    def is_valid(self):
        valid = super(AddChildForm, self).is_valid()
        if not valid:
            return valid
        child_age = self.cleaned_data['dob']
        age_of_child = datetime.date.today() - child_age
        if age_of_child.days < 1826:
            return True
        return False


class EditChildForm(forms.Form):
    """ form used to edit a childs information """
    childName = forms.CharField(label='Child Name', max_length=100, widget=forms.TextInput(attrs={'id':'childName'}))
    dob = forms.DateField(label='Child Date of Birth', widget=forms.DateInput(attrs={'id':'dob', 'type':'date'}))
    childID = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(EditChildForm, self).__init__(*args, **kwargs)
        self.fields['childName'].widget.attrs.update({'required': 'required'})
        self.fields['dob'].widget.attrs.update({'required': 'required', 'max':str(datetime.datetime.today().strftime('%Y-%m-%d'))})
    def is_valid(self):
        valid = super(EditChildForm, self).is_valid()
        if not valid:
            return valid
        child_age = self.cleaned_data['dob']
        age_of_child = datetime.date.today() - child_age
        if age_of_child.days < 1826:
            return True
        return False

class SubHeadingEditForm(forms.ModelForm):
    """ form used to edit a subheading """
    class Meta:
        """ meta information for this form """
        model = SubHeading
        widgets = {
            'text': RedactorEditor(),
            'ageGroup':forms.CheckboxSelectMultiple,
        }
        fields = '__all__'

class HeadingEditForm(forms.ModelForm):
    """ form used to edit a heading """
    class Meta:
        """ meta information for this form """
        model = Heading
        fields = '__all__'

class CategoryEditForm(forms.ModelForm):
    """ form used to edit a category """
    class Meta:
        """ meta information for this form """
        model = Category
        widgets = {
            'description': RedactorEditor(),
        }
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(CategoryEditForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False

class SearchForm(forms.Form):
    """ form used in the search view to get a query to search for """
    query = forms.CharField(label='Search Query', max_length=150, widget=forms.TextInput(attrs={'id':'query'}))

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs.update({'required': 'required'})

class DiaryLogEditForm(forms.ModelForm):
    """ form used to edit a diary log """
    class Meta:
        """ meta information for this form """
        model = DiaryLog
        fields = '__all__'
    check_id = forms.IntegerField()
    def __init__(self, *args, **kwargs):
        super(DiaryLogEditForm, self).__init__(*args, **kwargs)
        self.fields['child'].widget = HiddenInput()
        self.fields['check_id'].widget = HiddenInput()
