from django.shortcuts import render, redirect
from .models import Item
from .forms import InventoryForm, SaleForm, AddStockForm

# Create your views here.
def index(request):
    """ Home Page """
    return render(request, 'inventory/index.html')

def viewInventory(request):
    """ View inventory """
    inventorylist = Item.objects.order_by('id')
    context ={'inventory':inventorylist}
    return render(request, 'inventory/view-inventory.html', context)

def addInventory(request):
    """ Add a new inventory Item """
    if request.method != 'POST':
        # No data submitted; create blank form.
        form = InventoryForm()
    else:
        # POST data submitted; process data.
        form = InventoryForm(data=request.POST)
        if form.is_valid():
            #print("Form is valid") # Debugging
            instance = form.save(commit=False) # temp instance
            #print("Item before saving: ", instance.name, instance.quantity, instance.sell, instance.price)
            instance.save()
            #print("item Saved") # debugging
            form.save()
            return redirect('inventory:view-inventory')
        #else:
            #print("form errors:", form.errors)
    # Display blank or invalid form
    context = {'form':form}
    return render(request, 'inventory/add-inventory-item.html', context)

def record_sale(request):
    """Record a Sale and reduce inventory"""
    if request.method == 'POST':
        form = AddStockForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)  # Temporarily save sale
            item = sale.item  # Get the item being sold

            if sale.quantity > item.quantity:  # Check if sale exceeds stock
                return render(request, 'inventory/low-stock-warning.html', {'item': item, 'sale': sale})

            item.quantity -= sale.quantity  # Reduce stock
            item.save()
            sale.save()
            return redirect('inventory:view-inventory')

    else:
        form = AddStockForm()

    return render(request, 'inventory/record-sale.html', {'form': form})

def increaseInventory(request):
    """ Increase inventory quantity for an existing item """
    
    if request.method == 'POST':
        form = AddStockForm(data=request.POST)  # Form submission
        if form.is_valid():
            stock_update = form.save(commit=False)  # Temporary instance

            # Ensure item exists in the inventory
            item = stock_update.item  # Ensure AddStockForm includes an item field
            item.quantity += stock_update.quantity  # Increase inventory
            item.save()  # Save changes to the database
            stock_update.save()

            return redirect('inventory:view-inventory')  # Redirect back to inventory page

    else:
        form = AddStockForm()  # Empty form for GET requests

    context = {'form': form}
    return render(request, 'inventory/increase-inventory.html', context)