from django.db import models
from django.conf import settings


class Seller(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='seller',
    )
    store_name = models.CharField(max_length=255, unique=True)
    store_description = models.TextField()
    store_logo = models.ImageField(upload_to='store_logos/')
    store_address = models.CharField(max_length=255)
    store_city = models.CharField(max_length=100)
    store_state = models.CharField(max_length=100)
    store_country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    employee_id = models.CharField(max_length=100, unique=True)  # for verification

    def __str__(self):
        return self.store_name




class SellerReview(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.seller.store_name}"


class SalesAnalytics(models.Model):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    total_sales = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_orders = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sales Analytics for {self.seller.store_name}"

