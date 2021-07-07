from django import forms

from backend.settings import PAIRED_END_ENDING, SINGLE_END_ENDING


class BasicInputDDRadDataForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.restrictionEnzymes = kwargs.pop('restrictionEnzymes')
        super(BasicInputDDRadDataForm, self).__init__(*args, **kwargs)

        self.fields['fastaFile'].widget = forms.ClearableFileInput(attrs={'title': "",'class': 'form-control', 'id': 'fastaFileUpload', 'EnableViewState': "true"})

        restrictionEnzymesChoices = (('', '------'),) + tuple((index, enzyme.name) for index, enzyme in enumerate(self.restrictionEnzymes))
        self.fields['restrictionEnzyme1'].choices = restrictionEnzymesChoices
        self.fields['restrictionEnzyme2'].choices = restrictionEnzymesChoices
        self.initial['restrictionEnzyme1'] = ''
        self.initial['restrictionEnzyme2'] = ''

        self.fields['restrictionEnzyme3'].choices = restrictionEnzymesChoices
        self.fields['restrictionEnzyme4'].choices = restrictionEnzymesChoices
        self.initial['restrictionEnzyme3'] = ''
        self.initial['restrictionEnzyme4'] = ''

        self.fields['basepairLengthToBeSequenced'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        self.fields['pairedEndChoice'].choices = [(PAIRED_END_ENDING, 'Paired End'), (SINGLE_END_ENDING, 'Single End')]
        self.fields['sequencingYield'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        self.fields['coverage'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})


    fastaFile = forms.FileField()
    restrictionEnzyme1 = forms.ChoiceField(choices=[], label="Restriction Enzyme 1.1", required=False, widget=forms.Select(attrs={'title': '', 'class':'form-select'}))
    restrictionEnzyme2 = forms.ChoiceField(choices=[], label="Restriction Enzyme 1.2", required=False, widget=forms.Select(attrs={'title': "", 'class':'form-select'}))

    restrictionEnzyme3 = forms.ChoiceField(choices=[], label="Restriction Enzyme 2.1", required=False, widget=forms.Select(attrs={'class':'form-select'}))
    restrictionEnzyme4 = forms.ChoiceField(choices=[], label="Restriction Enzyme 2.2", required=False, widget=forms.Select(attrs={'class':'form-select'}))


    basepairLengthToBeSequenced = forms.CharField(label="Read length to be sequenced", required=False)
    pairedEndChoice = forms.ChoiceField(choices=[], widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    sequencingYield = forms.CharField(label="Sequencing Yield [reads]", required=False)
    coverage = forms.CharField(label="Coverage", required=False)