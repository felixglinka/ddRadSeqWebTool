from django import forms

from backend.settings import PAIRED_END_ENDING, SINGLE_END_ENDING, MAX_NUMBER_SELECTFIELDS


class BasicInputDDRadDataForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.restrictionEnzymes = kwargs.pop('restrictionEnzymes')
        super(BasicInputDDRadDataForm, self).__init__(*args, **kwargs)

        self.fields['fastaFile'].widget = forms.ClearableFileInput(attrs={'title': "",'class': 'form-control', 'id': 'fastaFileUpload', 'EnableViewState': "true"})

        restrictionEnzymesChoices = (('', '------'),) + tuple((index, enzyme.name) for index, enzyme in enumerate(self.restrictionEnzymes))
        for number in range(1, MAX_NUMBER_SELECTFIELDS):
            self.fields['restrictionEnzyme' + str(number)].choices = restrictionEnzymesChoices
            self.initial['restrictionEnzyme' + str(number)] = ''

        self.fields['basepairLengthToBeSequenced'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        self.fields['pairedEndChoice'].choices = [(PAIRED_END_ENDING, 'Paired End'), (SINGLE_END_ENDING, 'Single End')]
        self.fields['sequencingYield'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        self.fields['coverage'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})


    fastaFile = forms.FileField()

    for number in range(1, MAX_NUMBER_SELECTFIELDS):
        locals()[f"restrictionEnzyme{number}"] = forms.ChoiceField(choices=[], label="Restriction Enzyme "+str(int(number/2) if number % 2 == 0 else int(-(-(number/2) // 1)))+str('.')+str(2 if number % 2 == 0 else 1), required=False, widget=forms.Select(attrs={'class':'form-select'}))

    basepairLengthToBeSequenced = forms.CharField(label="Read length to be sequenced", required=False)
    pairedEndChoice = forms.ChoiceField(choices=[], widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    sequencingYield = forms.CharField(label="Sequencing Yield [reads]", required=False)
    coverage = forms.CharField(label="Coverage", required=False)