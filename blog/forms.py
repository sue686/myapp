from django import forms
from .models import Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ArticleAddForm(forms.ModelForm):

    title = forms.CharField()
    title.widget.attrs.update({'class': 'form-control'})
    content = forms.CharField(widget=CKEditorUploadingWidget())

    #
    # Email= forms.ChoiceField(choices=(('Y','Yes'), ('N','No')),
    #     initial='Y', widget=forms.RadioSelect)
    # email = forms.BooleanField(label='Send email to all staff?',required=False)



    class Meta:
        model = Post
        fields =['title','content']

    # def __init__(self, *args, **kwargs):
    #     super(ArticleAddForm, self).__init__(*args, **kwargs)
    #     self.fields['email'].value = True


class ArticleEditForm(forms.ModelForm):

    title = forms.CharField()
    title.widget.attrs.update({'class': 'form-control'})
    content = forms.CharField(widget=CKEditorUploadingWidget())

    email = forms.BooleanField(label='Send email to all staff?',required=False)
    # top = forms.BooleanField(label='Stick to the Top? Effective after General Manager consent',required=False)



    class Meta:
        model = Post
        fields =['title','content','email']
