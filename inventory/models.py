from django.db import models

# Create your models here.
class Item(models.Model):

    # Item in inventory
    ID = models.IntegerField()
    Description = models.CharField(max_length=200)
    Procurement_Price = models.FloatField()
    Sales_Price = models.FloatField()
    Length = models.IntegerField()


    def __str__(self):
        # Return a string representation of the model
        return self.text

class Entry(models.Model):
    # Entering in the item into inventory

    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Inventory Item'
    
    def __str__(self):
        # Return a string representation of the model
        return f"{self.text[:50]}..."