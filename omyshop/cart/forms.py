from django import forms


class CartAddProductForm(forms.Form):
    PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)  # Convert inputted value to int after validation.
    update = forms.BooleanField(required=False,
                                initial=False,  # False to add inputted quantity to existing quantity.
                                widget=forms.HiddenInput)
