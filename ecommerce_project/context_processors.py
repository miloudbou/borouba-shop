def cart_items(request):
    cart = request.session.get('cart', {})
    cart_items = []
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        cart_items.append({'product': product, 'quantity': quantity})

    # يمكنك إضافة بيانات أخرى هنا إذا كنت بحاجة لها
    return {
        'cart_items': cart_items,
        'site_name': 'بوروبة شوب',
        'discount': 10  # مثال على خصم إذا كنت ترغب في إضافته
    }

