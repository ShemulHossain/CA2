from django.shortcuts import redirect, render, get_object_or_404
from concert .models import Artist
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import stripe
from order.models import Order, OrderItem

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, artist_id):
    product = Artist.objects.get(id=artist_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()
    return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.ticket_price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total*100)
    description = 'Online Shop - New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    if request.method=='POST':
        print(request.POST)
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingcity = request.POST['stripeBillingAddressCity']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingcity = request.POST['stripeShippingAddressCity']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']

            customer = stripe.Customer.create(email=email,
                                            source=token)
            stripe.Charge.create(amount=stripe_total,
                                currency="eur",
                                description=description,
                                customer=customer.id)
            
            '''Creating the order'''
            try:
                order_details = Order.objects.create(
                        token = token,
                        total = total,
                        emailAddress = email,
                        billingName = billingName,
                        billingAddress1 = billingAddress1,
                        billingCity = billingcity,
                        billingCountry = billingCountry,
                        shippingName = shippingName,
                        shippingAddress1 = shippingAddress1, 
                        shippingCity = shippingcity,
                        shippingCountry = shippingCountry
                    )
                order_details.save()
                for order_item in cart_items:
                    oi = OrderItem.objects.create(
                        product = order_item.product.name,
                        quantity = order_item.quantity,
                        price = order_item.product.ticket_price,
                        order = order_details)
                    oi.save
                    '''Reduce stock when order is placed or saved'''
                    products = Artist.objects.get(id=order_item.product.id)
                    products.stock = int(order_item.product.stock - order_item.quantity)
                    products.save()
                    order_item.delete()
                    '''The terminal will print this message when the order is saved'''
                    print('The order has been created')
                return redirect ('order:thanks', order_details.id)

            except ObjectDoesNotExist:
                pass

        except stripe.error.CardError as e:
            return e
    return render(request, 'cart.html', {'cart_items':cart_items, 'total':total, 'counter':counter,
                                        'data_key':data_key, 'stripe_total':stripe_total,
                                        'description':description})


def cart_remove(request, artist_id):
    cart= Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Artist, id=artist_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')


def full_remove(request, artist_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Artist, id=artist_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')
