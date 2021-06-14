from django import forms

class BasicInputDDRadDataForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.restrictionEnzymes = kwargs.pop('restrictionEnzymes')
        super(BasicInputDDRadDataForm, self).__init__(*args, **kwargs)

        restrictionEnzymesChoices = (('', '------'),) + tuple((index, enzyme.name) for index, enzyme in enumerate(self.restrictionEnzymes))
        self.fields['restrictionEnzyme1'].choices = restrictionEnzymesChoices
        self.fields['restrictionEnzyme2'].choices = restrictionEnzymesChoices
        self.initial['restrictionEnzyme1'] = ''
        self.initial['restrictionEnzyme2'] = ''

        self.fields['restrictionEnzyme3'].choices = restrictionEnzymesChoices
        self.fields['restrictionEnzyme4'].choices = restrictionEnzymesChoices
        self.initial['restrictionEnzyme3'] = ''
        self.initial['restrictionEnzyme4'] = ''

        self.fields['sizeSelectMin'].widget = forms.TextInput(attrs={'autocomplete': 'off'})
        self.fields['sizeSelectMax'].widget = forms.TextInput(attrs={'autocomplete': 'off'})

    fastaFile = forms.FileField(label="")
    restrictionEnzyme1 = forms.ChoiceField(choices=[], label="Restriction Enzyme 1.1")
    restrictionEnzyme2 = forms.ChoiceField(choices=[], label="Restriction Enzyme 1.2")

    restrictionEnzyme3 = forms.ChoiceField(choices=[], label="Restriction Enzyme 2.1", required=False)
    restrictionEnzyme4 = forms.ChoiceField(choices=[], label="Restriction Enzyme 2.2", required=False)

    sizeSelectMin = forms.CharField(label="Minimum Size Selection", required=False)
    sizeSelectMax = forms.CharField(label="Maximum Size Selection", required=False)