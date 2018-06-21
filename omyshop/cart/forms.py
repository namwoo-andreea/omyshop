from django import forms


class CartAddProductForm(forms.Form):
    PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

    quantity = forms.ChoiceField(choices=PRODUCT_QUANTITY_CHOICES)
    update = forms.BooleanField(required=False,
                                initial=False,  # False to add inputted quantity to existing quantity.
                                widget=forms.HiddenInput)
