from django.db import models
from sellers.models import Seller
from django.contrib.auth.models import User



class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products_images/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    
    def get_discounted_price(self):
        return self.price - (self.price * self.discount / 100)



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    
    def __str__(self):
        return f'image for {self.product.name}'
    

class Category(models.Model):
    MAIN_CATEGORIES = [
        ("Gaming Consoles", "Gaming Consoles"),
        ("PC Gaming", "PC Gaming"),
        ("Gaming Accessories", "Gaming Accessories"),
        ("Games", "Games"),
        ("In-Game Items", "In-Game Items"),
        ("Gaming Peripherals", "Gaming Peripherals"),
        ("Streaming Equipment", "Streaming Equipment"),
        ("Merchandise", "Merchandise"),
        ("Mobile Gaming", "Mobile Gaming"),
        ("Gaming Subscriptions", "Gaming Subscriptions"),
        ("Board and Card Games", "Board and Card Games"),
        ("others", "others"),
    ]
    
    SUB_CATEGORIES = [
        # Gaming Consoles
        ("PlayStation", "PlayStation"),
        ("Xbox", "Xbox"),
        ("Nintendo", "Nintendo"),
        ("Retro Consoles", "Retro Consoles"),
        ("Handheld Consoles", "Handheld Consoles"),
        # PC Gaming
        ("Pre-built Gaming PCs", "Pre-built Gaming PCs"),
        ("Gaming Laptops", "Gaming Laptops"),
        ("Graphics Cards (GPUs)", "Graphics Cards (GPUs)"),
        ("Processors (CPUs)", "Processors (CPUs)"),
        ("Cooling Systems", "Cooling Systems"),
        # Gaming Accessories
        ("Controllers", "Controllers"),
        ("Gaming Mice", "Gaming Mice"),
        ("Keyboards", "Keyboards"),
        ("Headsets", "Headsets"),
        ("Gaming Chairs", "Gaming Chairs"),
        ("VR Accessories", "VR Accessories"),
        # Games
        ("Action", "Action"),
        ("Role-Playing Games (RPG)", "Role-Playing Games (RPG)"),
        ("Sports", "Sports"),
        ("Simulation", "Simulation"),
        ("Strategy", "Strategy"),
        ("Indie", "Indie"),
        ("VR Games", "VR Games"),
        # In-Game Items
        ("Virtual Currencies", "Virtual Currencies"),
        ("Skins", "Skins"),
        ("Weapons", "Weapons"),
        ("Characters", "Characters"),
        ("Bundles", "Bundles"),
        # Gaming Peripherals
        ("", "Gaming Peripherals"),
        ("Monitors", "Monitors"),
        ("Speakers", "Speakers"),
        ("Microphones", "Microphones"),
        ("Mouse Pads", "Mouse Pads"),
        ("External Storage", "External Storage"),
        # Streaming Equipment
        ("Capture Cards", "Capture Cards"),
        ("Lighting", "Lighting"),
        ("Streaming Microphones", "Streaming Microphones"),
        ("Camera/Facecam", "Camera/Facecam"),
        # Merchandise
        ("Apparel", "Apparel (T-Shirts, Hoodies, etc.)"),
        ("Action Figures", "Action Figures"),
        ("Posters", "Posters"),
        ("Collectibles", "Collectibles"),
        # Mobile Gaming
        ("Mobile Controllers", "Mobile Controllers"),
        ("Gaming Phones", "Gaming Phones"),
        ("Accessories", "Accessories (Stands, Cooling Pads, etc.)"),
        # Gaming Subscriptions
        ("Xbox Game Pass", "Xbox Game Pass"),
        ("PlayStation Plus", "PlayStation Plus"),
        ("Online Memberships", "Online Memberships"),
        # Board and Card Games
        ("Tabletop RPGs", "Tabletop RPGs"),
        ("Strategy Board Games", "Strategy Board Games"),
        ("Card Games", "Card Games"),
        ("Party Games", "Party Games"),
        # others
        ("others", "others"),
    ]
    
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, unique=True)
    parent_category = models.CharField(max_length=255, choices=MAIN_CATEGORIES)
    sub_category = models.CharField(max_length=255, choices=SUB_CATEGORIES)


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_categories')
    
    def __str__(self):
        return f'{self.product.name} - {self.category.name}'
    
    
    
    

    
