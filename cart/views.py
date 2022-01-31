from django.shortcuts import render,get_object_or_404,redirect
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from .models import Cart
from .models import CartItems
from bookstore.models import Book



def add_to_cart(request, user_book):
    session  = request.session.session_key

    print(session)
    if not session:
        session = request.session.create()

        cart_for_save = Cart.objects.create(
          cart_session=session,
         )
        cart_for_save.save()


    user_book=Book.objects.get(slug=user_book)
    session_aa = Cart.objects.get(cart_session=session)

    check_if_already_exits = CartItems.objects.all().filter(cart=session_aa, book=user_book).first()
    print(check_if_already_exits)


    if check_if_already_exits == None:


        cartitem_save = CartItems.objects.create(
          cart= Cart.objects.get(cart_session=session),
          book= Book.objects.get(slug=user_book),
          quantity=1,
          is_active=True,
          )
        cartitem_save.save()
    return redirect('cart')


def delete_cart_item(request, book_slug):
    session = request.session.session_key
    my_cart = Cart.objects.get(cart_session=session)
    cart_items = CartItems.objects.all().filter(cart=my_cart)
    for cart_item in cart_items:

        if cart_item.book.slug==book_slug:
            print(cart_item)
            cart_item.delete()






    return redirect('cart')


def cart(request):
    session = request.session.session_key
    cart_num = Cart.objects.get(cart_session=session)
    cart_items = CartItems.objects.all().filter(cart=cart_num)
    total=0
    for cart_item in cart_items:
        total += cart_item.book.price
    context = {
        'cart_items': cart_items,
        'total':total,

    }

    return render(request, "cart.html", context)





