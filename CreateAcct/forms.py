from django import forms

class InsertAcctForm(forms.Form):
    acct = forms.CharField(label='user', max_length=100)
