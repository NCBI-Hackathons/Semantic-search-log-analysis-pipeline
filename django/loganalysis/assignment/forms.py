from django import forms

class AssignmentForm(forms.Form):
    query_id = forms.CharField(label='query id')

class FuzzForm(forms.Form):
    query_id = forms.CharField(label='query id')
