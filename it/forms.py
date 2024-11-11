from django import forms
import datetime

from .models import Staffbirthday




class BirthdayaddForm(forms.ModelForm):

    # birthdaydate =  forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

    class Meta:
        model = Staffbirthday
        fields =['name','birthdaydate']
