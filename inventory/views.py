from django.shortcuts import render, redirect
from .models import Item
from .forms import InventoryForm, SaleForm

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
    return render(request, 'inventory/add-inventory.html', context)

def record_sale(request):
    """ Record a sale and update inventory quantity """
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)  # Get sale instance
            item = sale.item  # Get the selected inventory item

            if item.quantity >= sale.quantity:  # Ensure enough stock
                item.quantity -= sale.quantity  # Reduce stock
                item.save()  # Save updated inventory
                sale.save()  # Save the sale record
                return redirect('inventory:view-inventory')  # Redirect to inventory list
            else:
                form.add_error('quantity', 'Not enough stock available!')
    else:
        form = SaleForm()

    return render(request, 'inventory/record-sale.html', {'form': form})