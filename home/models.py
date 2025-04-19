from django.db import models
from django.contrib.auth.models  import User
import uuid;
from cloudinary.models import CloudinaryField

class BaseModel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True);
    created_at=models.DateTimeField(auto_now_add=True);
    updated_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract=True;
        
class PizzaCategory(BaseModel):
    category_name=models.CharField(max_length=100);


class Pizza(BaseModel):
    category_name=models.ForeignKey(PizzaCategory,on_delete=models.CASCADE,related_name="pizzas");
    Pizza_name=models.CharField(max_length=100);
    price=models.IntegerField(default=100)
    images=CloudinaryField('images')
    
class Cart(BaseModel):
    user=models.ForeignKey(User,null=True ,blank=True, on_delete=models.SET_NULL,related_name='carts');
    is_paid=models.BooleanField(default=False)
    
class CartItems(BaseModel):    
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='carts_items');
    Pizza=models.ForeignKey(Pizza,on_delete=models.CASCADE);
    
   
