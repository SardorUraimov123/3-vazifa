from django.shortcuts import render, redirect
from main import models

def index(request):
    context = {}
    return render(request, 'dashboard/index.html', context)

# ---------CATEGORY-------------


def category_list(request):
        queryset = models.Category.objects.all()
        context = {
            'queryset':queryset
            }
        return render(request, 'dashboard/category/list.html', context)


def category_create(request):
    if request.method == 'POST':
        models.Category.objects.create(
            name = request.POST['name']
        )
        return redirect('dashboard:category_list')
    return render(request, 'dashboard/category/create.html')


def category_update(request, id):
    queryset = models.Category.objects.get(id=id)
    queryset.name = request.POST['name']
    queryset.save()
    return redirect('dashboard:category_detail', queryset.id)


def category_delete(request, id):
    queryset = models.Category.objects.get(id=id)
    queryset.delete()
    return redirect('dashboard:category_list')

# ---------PRODUCT----------------

def product_list(request):
    queryset = models.Product.objects.all()
    context = {
          'queryset':queryset
    }
    return render(request, 'dashboard/product/list.html', context)


def product_detail(request, id):
    queryset = models.Product.objects.get(id=id)
    images = models.ProductImg.objects.filter(product=queryset)
    reviews = models.Review.objects.filter(product=queryset)
    context = {
          'queryset':queryset,
          'images':images,
          'reviews':reviews
    }
    return render(request, 'dashboard/product/detail.html', context)
    

def product_create(request):
    categorys = models.Category.objects.all()
    context = {'categorys': categorys}
    if request.method == 'POST':
        delivery = True if request.POST.get('delivery') else False

        banner_img = request.FILES.get('banner_img')
        video = request.FILES.get('video')

        product = models.Product.objects.create(
            category_id=request.POST['category_id'],
            name=request.POST['name'],
            body=request.POST['body'],
            price=request.POST['price'],
            quantity=request.POST['quantity'],
            delivery=delivery
        )
        if banner_img:
            product.banner_img = banner_img
        if video:
            product.video = video

        product.save()

        return redirect('dashboard:product_list')
    return render(request, 'dashboard/product/create.html', context)


def product_update(request, id):
    product = models.Product.objects.get(id=id)

    if request.method == 'POST':
        product.category_id = request.POST['category_id']
        product.name = request.POST['name']
        product.body = request.POST['body']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        product.delivery = request.POST.get('delivery', False) 
        
        if 'banner_img' in request.FILES:
            product.banner_img = request.FILES['banner_img']
        
        if 'video' in request.FILES:
            product.video = request.FILES['video']

        product.save()
        return redirect('dashboard:product_list')

    context = {'product': product}
    return render(request, 'dashboard/product/update.html', context)



def product_delete(request, id):
    product = models.Product.objects.get(id=id)
    product.delete()
    return redirect('dashboard:product_list')