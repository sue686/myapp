from django import forms
from .models import FileInfo,Category


class ViewForm(forms.ModelForm):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),  # 支持多文件上传
        label='Select File...',
        help_text='limit:10M'
        )
    file.widget.attrs.update({'class': 'custom-select documents-custom'})
    # file.widget.attrs.update({'class':'documents-custom'})

    # categoryname = forms.ModelChoiceField(queryset=Category.objects.values_list('categoryname', flat=True).distinct())
    categoryname = forms.ModelChoiceField(queryset=Category.objects.all(),label='Category')
    categoryname.widget.attrs.update({'class': 'custom-select documents-custom'})

    class Meta:
        model = Category
        fields =['categoryname']

    def __init__(self, department,campus,*args, **kwargs):
        super(ViewForm, self).__init__(*args, **kwargs)
        self.fields['categoryname'].queryset = Category.objects.filter(department=department,campus=campus)

class UploadForm(forms.ModelForm):

    class Meta:
        model = FileInfo
        fields =['filename','filesize','campus',]


class CategoryForm(forms.ModelForm):


    class Meta:
        model = Category
        fields =['categoryname']


class CategoryUpdateForm(forms.ModelForm):

    class Meta:
        model = Category
        fields =['categoryname']
