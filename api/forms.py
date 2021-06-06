from django import forms

from backend.controller.ddRadtoolController import requestRestrictionEnzymes


class BasicInputDDRadDataForm(forms.Form):

    restrictionEnzymes = tuple(enzyme.name for enzyme in requestRestrictionEnzymes())

    DEMO_CHOICES = (
        "Naveen",
        "Pranav",
    )

    fastaFile = forms.FileField(label="")
    restrictionEnzyme1 = forms.ChoiceField(choices = DEMO_CHOICES, label="")
    #restrictionEnzyme2 = forms.MultipleChoiceField(choices=restrictionEnzymes, label="")
