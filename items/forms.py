from django import forms

from .models import ItemRef

Choices = [
    (0, 'Mercado'),
    (1, 'Farmacia'),
]


class ItemForm(forms.ModelForm):
    class Meta:
        model = ItemRef
        fields = '__all__'

    name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'placeholder': 'Nome do produto', 'class': 'input-name'}))
    type = forms.CharField(max_length=128, widget=forms.Select(
        choices=Choices, attrs={'placeholder': 'Selecte o tipo de loja do profuto', 'class': 'select-type'}))
    validate = forms.IntegerField(widget=forms.NumberInput(
        attrs={'placeholder': 'Quantos dias dura este produto?', 'class': 'input-validate'}))
