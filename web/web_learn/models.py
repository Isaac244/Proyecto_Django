from django.db import models

# Create your models here.
class Producto(models.Model):
    prod = models.CharField(
        verbose_name="Producto",
        blank=False,
        max_length=255,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return str(self.prod)
    
class ProductRecomender(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
    )
    position = models.CharField(
        max_length=255,
        blank=False,
    )
    create_at = models.DateTimeField(
        auto_now_add=True
    )