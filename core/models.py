from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    message=models.TextField()
    email=models.EmailField()

class Category(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to="category_images",null=True)
    
    def __str__(self):
        return self.title
    
class Momo(models.Model):
    name=models.CharField(max_length=200) #buff fried momo
    category=models.ForeignKey(Category, on_delete=models.CASCADE,related_name="items") #buff
    desc=models.TextField()
    price=models.DecimalField(max_digits=8,decimal_places=2)
    image=models.ImageField(upload_to="images")
    is_available=models.BooleanField(default=True)
    created_at=models.DateField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    
    # modelapi, formapi
class Review(models.Model):
    name=models.CharField(max_length=200)
    message=models.TextField()
    order=models.CharField(max_length=200)
    rating=models.PositiveSmallIntegerField()
    
    