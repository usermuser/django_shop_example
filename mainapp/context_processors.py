from basket.models import Basket

def basket(request):
    print('[+] Context processor basket works')
    basket = []

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        # print('basket:', basket)

    return {'basket': basket, }