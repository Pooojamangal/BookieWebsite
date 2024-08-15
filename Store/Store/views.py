from django.shortcuts import redirect, render ,get_object_or_404
from django.http import HttpRequest , HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from add_books.models import AddBook
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation


def welcome(request):
    return render(request,"index.html")
def user_login(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user )
            name = getattr(user, 'name', 'User')
            messages.success(request, "Logged In Successfully!")
            return render(request, "dashboard.html", {"Name": name})
        else:
            messages.error(request, "Bad Credentials!")
            return redirect("login")

    return render(request, 'login.html')
def signup(request):  
    if request.method == 'POST':
        username = request.POST['Username']
        name = request.POST['Name']
        email = request.POST['Email']
        password = request.POST['Password']
        password1 = request.POST['Password1']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('home')

        myuser = User.objects.create_user(username,email,password)
        myuser.Name = name
        myuser.save()

        messages.success(request, 'Your Account Has been Succesfully Created!!')
        return redirect('login')

    return render(request, 'signup.html')
def signout(request): 
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')
    #return render(request, 'signout.html')
def joinus(request):
    return render(request, 'Joinus.html')
def books(request):
    return render(request, 'books.html')
def cart(request):
    return render(request, "cart.html")
def order(request):
    return render(request, 'order.html')
def checkout(request):
    return render(request, 'checkout.html')

@login_required
def dashboard(request):
    # Fetch all books
    books = AddBook.objects.all()
    context = {
        'books': books,
    }
    return render(request, 'dashboard.html', context)

def addbooks(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        price = request.POST['price']
        image = request.FILES['image']
        try:
            price_input = request.POST['price']
            if price_input.strip() == "":
                raise InvalidOperation("Price field is empty.")
            price = Decimal(price_input)
        except InvalidOperation:
            messages.error(request, "Invalid price format. Please enter a valid decimal number.")
            return render(request, 'addbooks.html')

        book = AddBook(title=title, author=author, price=price, image=image)
        book.save()

        messages.success(request, 'Book added successfully!')
        return redirect('dashboard')  

    return render(request, 'addbooks.html')  

@login_required

def editbook(request, book_id):
    book = get_object_or_404(AddBook, id=book_id)

    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.price = request.POST['price']
        
        if 'image' in request.FILES:
            book.image = request.FILES['image']
        
        book.save()
        messages.success(request, 'Book updated successfully!')
        return redirect('dashboard')

    context = {'book': book}
    return render(request, 'edit.html', context)

@login_required
def deletebook(request, book_id):
    book = get_object_or_404(AddBook, id=book_id)
    book.delete()
    messages.success(request, 'Book deleted successfully!')
    return redirect('dashboard')