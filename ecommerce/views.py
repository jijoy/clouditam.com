import iyzipay
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def test(request):
    options = dict([('base_url', 'sandbox-api.iyzipay.com')])
    options['api_key'] = 'sandbox-dNFYc1n5q3uHgDGQUFPSQJOUFvGB4zib'
    options['secret_key'] = 'sandbox-mYBFuDEvMhk7ojzyrg7VkkhJ5lkShdz8'

    test = dict([('locale', 'tr')])
    test['conversationId'] = '123456789'
    test['price'] = '1'
    test['paidPrice'] = '1.1'
    test['installment'] = '1'
    test['basketId'] = 'B67832'
    test['paymentChannel'] = 'WEB'
    test['paymentGroup'] = 'PRODUCT'
    test['callbackUrl'] = 'http://127.0.0.1:8000/callback'
    test['currency'] = 'TRY'

    payment_card = dict([('cardHolderName', 'John Doe')])
    payment_card['cardNumber'] = '5528790000000008'
    payment_card['expireMonth'] = '12'
    payment_card['expireYear'] = '2030'
    payment_card['cvc'] = '123'
    payment_card['registerCard'] = '0'
    test['paymentCard'] = payment_card

    buyer = dict([('id', 'BY789')])
    buyer['name'] = 'John'
    buyer['surname'] = 'Doe'
    buyer['gsmNumber'] = '+905350000000'
    buyer['email'] = 'email@email.com'
    buyer['identityNumber'] = '74300864791'
    buyer['lastLoginDate'] = '2015-10-05 12:43:35'
    buyer['registrationDate'] = '2013-04-21 15:12:09'
    buyer['registrationAddress'] = 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1'
    buyer['ip'] = '85.34.78.112'
    buyer['city'] = 'Istanbul'
    buyer['country'] = 'Turkey'
    buyer['zipCode'] = '34732'
    test['buyer'] = buyer

    address = dict([('address', 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1')])
    address['zipCode'] = '34732'
    address['contactName'] = 'Jane Doe'
    address['city'] = 'Istanbul'
    address['country'] = 'Turkey'
    test['shippingAddress'] = address
    test['billingAddress'] = address

    basket_items = []
    basket_item_first = dict([('id', 'BI101')])
    basket_item_first['name'] = 'Binocular'
    basket_item_first['category1'] = 'Collectibles'
    basket_item_first['category2'] = 'Accessories'
    basket_item_first['itemType'] = 'PHYSICAL'
    basket_item_first['price'] = '0.3'
    basket_items.append(basket_item_first)

    basket_item_second = dict([('id', 'BI102')])
    basket_item_second['name'] = 'Game code'
    basket_item_second['category1'] = 'Game'
    basket_item_second['category2'] = 'Online Game Items'
    basket_item_second['itemType'] = 'VIRTUAL'
    basket_item_second['price'] = '0.5'
    basket_items.append(basket_item_second)

    basket_item_third = dict([('id', 'BI103')])
    basket_item_third['name'] = 'Usb'
    basket_item_third['category1'] = 'Electronics'
    basket_item_third['category2'] = 'Usb / Cable'
    basket_item_third['itemType'] = 'PHYSICAL'
    basket_item_third['price'] = '0.2'
    basket_items.append(basket_item_third)

    test['basketItems'] = basket_items

    # make test
    payment_auth = iyzipay.PaymentAuth()
    payment_auth_response = payment_auth.create(test, options)
    return HttpResponse(payment_auth_response)