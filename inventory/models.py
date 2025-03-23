from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField()
    sell = models.FloatField()
    quantity = models.IntegerField()
    time = models.IntegerField()



    def __str__(self):
        # Return a string representation of the model
        return self.name  #Description

class Sale(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE) # Link Sale to an Intem
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - {self.quantity} sold"