var form = document.querySelector('#payment')
var submit = document.querySelector('input[type="submit"]')

braintree.client.create({
    authorization: clientToken
}, function (clientErr, clientInstance) {
    if (clientErr) {
        console.error(clientErr);
        return;
    }

    braintree.hostedFields.create({
        client: clientInstance,
        styles: {
            'input': {'font-size': '13px'},
            'input.invalid': {'color': 'red'},
            'input,valid': {'color': 'green'}
        },
        fields: {
            number: {selector: '#card-number'},
            cvv: {selector: '#cvv'},
            expirationDate: {selector: '#expiration-date'}
        }
    }, function (hostedFieldsErr, hostedFieldsInstance) {
        if (hostedFieldsErr) {
            console.error(hostedFieldsErr)
            return;
        }

        submit.removeAttribute('disabled');

        form.addEventListener('submit', function (event) {
            event.preventDefault();

            hostedFieldsInstance.tokenize(function (tokenizeErr, payload) {
                if (tokenizeErr) {
                    console.error(tokenizeErr)
                    return;
                }

                document.getElementById('nonce').value = payload.nonce;
                document.getElementById('payment').submit();
            });
        }, false);
    });
});