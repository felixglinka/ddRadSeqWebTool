from django import forms

class BasicInputDDRadDataForm(forms.Form):
    fastaFile = forms.FileField(label="")
    #restrictionEnzyme1 = forms.ChoiceField(label="")
    #restrictionEnzyme2 = forms.ChoiceField(label="")