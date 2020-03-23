from django import forms

class ImageForm(forms.Form):
    uploadedImage = forms.FileField()
