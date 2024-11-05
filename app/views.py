from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
import razorpay
from . models import Cart,Customer, OrderPlaced,Payment, Wishlist,product
from . forms import CustomerProfileForm,CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.utils import timezone 
from .models import RecentlyViewed
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

def home(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/home.html",locals())

def about(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))        
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/about.html",locals())

def contact(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/contact.html",locals())

class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        wishitem = 0
        cart_items = []
        
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()
            wishitem = Wishlist.objects.filter(user=request.user).count()
            # Get the list of product IDs already in the cart
            cart_items = Cart.objects.filter(user=request.user).values_list('Product_id', flat=True)
        
        # Filter products based on the selected category
        Product = product.objects.filter(category=val)
        # Get distinct titles and count of products by title
        title = product.objects.filter(category=val).values('title').annotate(total=Count('title'))
        
        # Pass the cart_items list to the template
        return render(request, "app/category.html", locals())

    
class CategoryTitle(View):
    def get(self,request,val):
        Product = product.objects.filter(title=val)
        title = product.objects.filter(category=Product[0].category).values('title')    
        totalitem = 0
        wishitem=0
        cart_items = []
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user).values_list('Product_id', flat=True)
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request,"app/category.html",locals())
    
@method_decorator(login_required,name='dispatch')
class RecentlyViewedView(View):
    def get(self, request):    
        totalitem = 0
        wishitem=0
        cart_items =[]

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
            cart_items = Cart.objects.filter(user=request.user).values_list('Product_id', flat=True)

        # Get recently viewed products for the user
        recently_viewed = RecentlyViewed.objects.filter(user=request.user).select_related('Product')[:10]  # Limit to the 10 most recent
        return render(request, 'app/recently_viewed.html',{'recently_viewed': recently_viewed,'cart_items':cart_items, 'totalitem': totalitem ,'wishitem':wishitem})

@method_decorator(login_required,name='dispatch')
class wishlist(View):
    def get(self, request):    
        totalitem = 0
        wishitem=0
        wishlist_items = []
        cart_items = []

        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()
            wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
            wishitem=len(Wishlist.objects.filter(user=request.user))
            cart_items = Cart.objects.filter(user=request.user).values_list('Product_id', flat=True)

        recently_viewed = RecentlyViewed.objects.filter(user=request.user).select_related('Product')[:10]  # Limit to the 10 most recent
        # Get recently viewed products for the user
        return render(request, 'app/wishlist.html',{'wishlist_items': wishlist_items,'recently_viewed':recently_viewed,'cart_items':cart_items, 'totalitem': totalitem ,'wishitem':wishitem})

@method_decorator(login_required,name='dispatch')
class ProductDetail(View):

    def get(self, request, pk):
        Product = product.objects.get(pk=pk)  # Use 'Product' as the variable name
        cart_items = Cart.objects.filter(user=request.user).values_list('Product_id', flat=True)
        totalitem = 0
        wishitem=0
        cart_item = None
        similar_products = product.objects.filter(category=Product.category).exclude(id=Product.id)[:10]
        
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
            cart_item = Cart.objects.filter(user=request.user, Product=Product).exists()
            all_products = product.objects.all()

            # Save to RecentlyViewed, but avoid duplicates
            recently_viewed, created = RecentlyViewed.objects.get_or_create(user=request.user, Product=Product)
            wishlist = Wishlist.objects.filter(user=request.user, product=Product).exists()
            # Update the viewed time if the product was already viewed
            if not created:
                recently_viewed.viewed_at = timezone.now()
                recently_viewed.save()            
        else:
            wishlist = False
        
            context = {
                'cart_item':cart_item,
                'all_products':all_products,
                'similar_products': similar_products,
                'Product': Product,
                'cart_items': cart_items,
                'wishlist': wishlist
            }
            if not created:
                # Update the `viewed_at` time if it already exists
                recently_viewed.viewed_at = timezone.now()
                recently_viewed.save()
        return render(request,"app/productdetail.html",locals())

class CustomerRegistrationView(View):
    def get(self,request):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/customerregistration.html',locals())
    
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Save Successfuly")
        else:
            messages.warning(request,"Invalid Input Data ")
        return render(request, 'app/profile.html',locals())


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/address.html',locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulation! Profile Update Successfuly")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")

@login_required 
def show_cart(request):
    cart_items = []
    wishlist_items = []
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        
        totalitem = len(cart)  # Count of items in the cart
        wishitem = len(Wishlist.objects.filter(user=user))  # Count of wishlist items
        amount = 0
        
        # Calculate total amount
        for p in cart:
            value = p.quantity * p.Product.discount_price
            amount += value
        
        totalamount = amount + 40  # Include any additional charges (like shipping)                
        recently_viewed = RecentlyViewed.objects.filter(user=user).select_related('Product')[:10]
        cart_items = Cart.objects.filter(user=request.user).values_list('Product_id', flat=True)
        wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')


        # Render the cart page
        return render(request, 'app/addtocart.html', {
            'cart': cart,
            'amount': amount,
            'totalitem': totalitem,
            'wishitem': wishitem,
            'totalamount': totalamount,
            'recently_viewed': recently_viewed, 
            'cart_items':cart_items,
            'wishlist_items':wishlist_items,
        })
    else:
        return redirect('login')  # Redirect to login if the user is not authenticated
  # Redirect to login page if user is not authenticated

@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.Product.discount_price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = { "amount": razoramount, "currency":"INR","receipt":"order_rcptid_12"}
        payment_responce =  client.order.create(data=data)
        #{'amount': 13000, 'amount_due': 13000, 'amount_paid': 0, 'attempts': 0, 'created_at': 1727871814, 'currency': 'INR', 'entity': 'order', 'id': 'order_P4ATTNIdczVKz0', 'notes': [], 'offer_id': None, 'receipt': 'order_rcptid_12', 'status': 'created'}
        order_id = payment_responce['id']
        order_status = payment_responce['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        if not cart_items:  # Check if the cart is empty
            return redirect('/')
        return render(request, 'app/chekout.html',locals())

@login_required
def payment_done(request):
    order_id=request.GET.get('order_id') 
    payment_id=request.GET.get('payment_id') 
    cust_id=request.GET.get('cust_id')

    user=request.user
    customer=Customer.objects.get(id=cust_id)
    payment =Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    #To save order details
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced (user=user, customer=customer, product=c.Product, quantity=c.quantity,payment=payment).save() 
        c.delete() 
    return redirect("orders")

@login_required
def orders(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(Product=prod_id) & Q(user=request.user))
        c.quantity +=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.Product.discount_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        
        # Get the cart item for the current user and product
        cart_item = get_object_or_404(Cart, Q(Product=prod_id) & Q(user=request.user))
        
        cart_item.quantity -= 1
        
        if cart_item.quantity <= 0:
            # Remove the item from the cart if quantity is zero
            cart_item.delete()
            quantity = 0  # Set quantity to 0 since the item was removed
        else:
            # Save the cart item if it still has quantity left
            cart_item.save()
            quantity = cart_item.quantity
        
        # Calculate total amount
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.Product.discount_price
            amount += value
        
        # Include additional charges (like shipping)
        totalamount = amount + 40
        
        # Prepare the response data
        data = {
            'quantity': quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        
        return JsonResponse(data)
 
@login_required       
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(Product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.Product.discount_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@login_required 
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        Product=product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=Product).save()
        data={
            'message':'Wishlist Added Successfully',
        }
        return JsonResponse(data)
    
@login_required 
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        Product=product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=Product).delete()
        data={
            'message':'Wishlist Removed Successfully',
        }
        return JsonResponse(data)
    
def search(request):
    # Use .get() method to avoid MultiValueDictKeyError
    query = request.GET.get('search', '').strip()  # Safely get 'search' and trim any spaces
    search_item = product.objects.filter(title__icontains=query) if query else None  # Your search logic here
    totalitem = 0
    wishitem = 0
    Product = []  # Initialize as an empty list
    
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = Wishlist.objects.filter(user=request.user).count()

    # Only search if there's a non-empty query
    if query:
        Product = product.objects.filter(Q(title__icontains=query))

    return render(request, "app/search.html", {
        'Product': Product,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'query': query,
        'search_item':search_item
    })

@method_decorator(login_required,name='dispatch')
class BuyNow(View):
    def get(self, request, product_id):
        user = request.user
        # Get the product or return 404 if not found
        Product = get_object_or_404(product, id=product_id)
        
        # Check if the product is already in the cart
        existing_cart_item = Cart.objects.filter(user=user, Product=Product).first()
        
        if not existing_cart_item:
            # Add the product to the cart if it's not already there
            Cart.objects.create(user=user, Product=Product)
        
        # Redirect to the checkout page
        return redirect('checkout')
 
def get_cart_data(user):
    cart_items = Cart.objects.filter(user=user)  # Filter by current user
    items = []
    total_amount = 0

    for item in cart_items:
        items.append({
            'product_id': item.Product.id,
            'product_name': item.Product.title,
            'product_image': item.Product.product_image.url,
            'quantity': item.quantity,
            'total_price': item.Product.discount_price * item.quantity,
        })
        total_amount += item.Product.discount_price * item.quantity

    return {
        'success': True,
        'cart_items': items,
        'amount': total_amount,
        'totalamount': total_amount + 40,  # Add shipping cost or other adjustments
    }

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    Product = product.objects.get(id=product_id)
    existing_cart_item = Cart.objects.filter(user=user, Product=Product).first()

    if existing_cart_item:
        existing_cart_item.quantity += 1
        existing_cart_item.save()
    else:
        Cart.objects.create(user=user, Product=Product)
           # Calculate total amount and total quantity
    return JsonResponse(get_cart_data(user))

def update_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    action = request.GET.get('action')
    
    if not product_id:
        return JsonResponse({'success': False, 'error': 'Product ID is missing.'})

    try:
        cart_item = Cart.objects.get(user=user,Product__id=product_id)
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cart item not found.'})

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        elif cart_item.quantity == 1:
            # Remove the item from the cart if the quantity reaches zero
            cart_item.delete()
            # Return updated cart data
            return JsonResponse(get_cart_data(user), safe=False)

    cart_item.save()

    # Return updated cart data
    return JsonResponse(get_cart_data(user))

 
def remove_from_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')

    try:
        cart_item = Cart.objects.get(user=user, Product__id=product_id)
        cart_item.delete()
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cart item not found.'})

    # Return updated cart data
    return JsonResponse(get_cart_data(user)) 
  # Assuming you have a Product model

def all_products_view(request):
    totalitem = 0
    wishitem = 0
    cart_items = []
    
    if request.user.is_authenticated:
        # Get the total number of items in the user's cart and wishlist
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = Wishlist.objects.filter(user=request.user).count()
        # Get the list of product IDs already in the cart
        cart_items = Cart.objects.filter(user=request.user).values_list('Product_id', flat=True)

    # Fetch all products
    Products = product.objects.all()
    # Get distinct titles and count of products by title
    title = product.objects.values('title').annotate(total=Count('title'))

    # Pass the cart_items list to the template
    return render(request, 'app/all_products.html', {
        'Products': Products,
        'title': title,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'cart_items': cart_items,
    })



def logout_and_reset_password(request):
    logout(request)  # Logs out the current user
    return redirect(reverse('password_reset'))  # Redirects to the password reset page