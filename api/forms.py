from django import forms

from backend.controller.ddRadtoolController import requestRestrictionEnzymes


class BasicInputDDRadDataForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.restrictionEnzymes = kwargs.pop('restrictionEnzymes')
        super(BasicInputDDRadDataForm, self).__init__(*args, **kwargs)

        restrictionEnzymesChoices = (('', '------'),) + tuple((index, enzyme.name) for index, enzyme in enumerate(self.restrictionEnzymes))
        self.fields['restrictionEnzyme1'].choices = restrictionEnzymesChoices
        self.fields['restrictionEnzyme2'].choices = restrictionEnzymesChoices
        self.initial['restrictionEnzyme1'] = ''
        self.initial['restrictionEnzyme2'] = ''

    fastaFile = forms.FileField(label="")
    restrictionEnzyme1 = forms.ChoiceField(choices=[], label="Restriction Enzyme 1")
    restrictionEnzyme2 = forms.ChoiceField(choices=[], label="Restriction Enzyme 2")


