from django import forms

from backend.settings import PAIRED_END_ENDING, SINGLE_END_ENDING, MAX_NUMBER_SELECTFIELDS


class BasicInputDDRadDataForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.restrictionEnzymes = kwargs.pop('restrictionEnzymes')
        super(BasicInputDDRadDataForm, self).__init__(*args, **kwargs)

        self.fields['popStructNumberOfSnps'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        self.fields['popStructExpectPolyMorph'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        self.fields['genomeScanExpectPolyMorph'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        self.fields['genomeScanRadSnpDensity'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        self.fields['linkageMappingNumberOfSnps'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})

        restrictionEnzymesChoices = (('', '------'),) + tuple((index, enzyme.name) for index, enzyme in enumerate(self.restrictionEnzymes))
        for number in range(1, MAX_NUMBER_SELECTFIELDS):
            self.fields['restrictionEnzyme' + str(number)].choices = restrictionEnzymesChoices
            self.initial['restrictionEnzyme' + str(number)] = ''

        self.fields['basepairLengthToBeSequenced'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        self.fields['pairedEndChoice'].choices = [(PAIRED_END_ENDING, 'Paired end'), (SINGLE_END_ENDING, 'Single end')]
        self.fields['sequencingYield'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        self.fields['coverage'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        self.fields['tryOutExpectPolyMorph'].widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})

    formFile = forms.CharField(widget=forms.HiddenInput(), required=False)
    formFileName = forms.CharField(widget=forms.HiddenInput(), required=False)
    formMode = forms.CharField(widget=forms.HiddenInput(), required=False)

    popStructNumberOfSnps = forms.CharField(label="Number of SNPs to be genotyped", required=False)
    popStructExpectPolyMorph = forms.CharField(label="Expected SNP density", required=False)
    genomeScanExpectPolyMorph = forms.CharField(label="Expected SNP density", required=False)
    genomeScanRadSnpDensity = forms.CharField(label="Desired SNP density to be genotyped", required=False)
    linkageMappingNumberOfSnps = forms.CharField(label="Number Of SNPs to be sequenced ", required=False)

    for number in range(1, MAX_NUMBER_SELECTFIELDS):
        locals()[f"restrictionEnzyme{number}"] = forms.ChoiceField(choices=[], label="Restriction enzyme "+str(int(number/2) if number % 2 == 0 else int(-(-(number/2) // 1)))+str('.')+str(2 if number % 2 == 0 else 1), required=False, widget=forms.Select(attrs={'class':'form-select'}))

    basepairLengthToBeSequenced = forms.CharField(label="Read length to be sequenced", required=False)
    pairedEndChoice = forms.ChoiceField(choices=[], widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), required=False)
    sequencingYield = forms.CharField(label="Sequencing yield", required=False)
    coverage = forms.CharField(label="Desired depth", required=False)
    tryOutExpectPolyMorph = forms.CharField(label="Expected SNP density", required=False)
