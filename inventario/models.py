from django.db import models
from decimal import Decimal
from django.utils.timezone import now
from django.db.models import Sum, F, FloatField
from django.contrib.auth.models import User


class Caja(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    monto_cierre = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    abierta = models.BooleanField(default=True)
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # <-- agregar

    def __str__(self):
        return f"Caja de {self.usuario.username} - {self.fecha_apertura.date()}"


class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    documento = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    marca = models.CharField(max_length=200)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField() 
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unidad_medida = models.CharField(max_length=20, blank=True)
    precio_compra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    porcentaje_ganancia = models.DecimalField(max_digits=5, decimal_places=2, default=30)  # % por defecto
    total_inversion = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ganancia = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # editable al registrar venta

    def save(self, *args, **kwargs):
        self.precio_compra = Decimal(self.precio_compra or 0)
        self.porcentaje_ganancia = Decimal(self.porcentaje_ganancia or 0)
        self.cantidad = Decimal(self.cantidad or 0)

        if self.precio_compra > 0:
            self.precio_venta = self.precio_compra * (1 + self.porcentaje_ganancia / Decimal(100))
        else:
            self.precio_venta = Decimal(0)

        self.total_inversion = self.cantidad * self.precio_compra
        self.ganancia = self.cantidad * (self.precio_venta - self.precio_compra)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.marca})"

# ========================
# MODELOS DE VENTA
# ========================

from decimal import Decimal
from django.db import models
from django.db.models import Sum, F, FloatField

class Sale(models.Model):
    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE)
    tipo_comprobante = models.CharField(
        max_length=50,
        choices=[
            ("Nota", "Nota de Venta"),
            ("Boleta", "Boleta"),
            ("Factura", "Factura"),
        ]
    )
    fecha = models.DateTimeField(auto_now_add=True)
    numero_venta = models.PositiveIntegerField(unique=True, blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    caja = models.ForeignKey("Caja", on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        from .models import Caja  # dentro de la función para evitar circularidad

        # ----------------------------
        # 1️⃣ Número de venta consecutivo
        # ----------------------------
        if not self.numero_venta:
            last_sale = Sale.objects.order_by('-numero_venta').first()
            self.numero_venta = 1 if not last_sale else last_sale.numero_venta + 1

        # ----------------------------
        # 2️⃣ Guardar datos previos si es edición
        # ----------------------------
        is_new = self.pk is None
        previous_total = Decimal("0.00")
        previous_caja = None

        if not is_new:
            prev = Sale.objects.get(pk=self.pk)
            previous_total = prev.total
            previous_caja = prev.caja

        # ----------------------------
        # 3️⃣ Guardar la venta primero para tener pk
        # ----------------------------
        if is_new:
            super().save(*args, **kwargs)

        # ----------------------------
        # 4️⃣ Calcular total de la venta
        # ----------------------------
        total_calculado = self.items.aggregate(
            total=Sum(F('cantidad') * F('precio'), output_field=FloatField())
        )['total'] or 0
        self.total = Decimal(str(total_calculado))

        # ----------------------------
        # 5️⃣ Asignar caja abierta si no tiene
        # ----------------------------
        if not self.caja:
            caja_abierta = Caja.objects.filter(abierta=True).first()
            if caja_abierta:
                self.caja = caja_abierta

        # ----------------------------
        # 6️⃣ Guardar venta con total actualizado
        # ----------------------------
        super().save(update_fields=['total', 'caja'])

        # ----------------------------
        # 7️⃣ Ajustar total de la caja correctamente
        # ----------------------------
        if self.caja and self.caja.abierta:
            if self.caja.total is None:
                self.caja.total = Decimal("0.00")

            if is_new:
                # Nueva venta → sumar total a la caja
                self.caja.total += self.total
            else:
                # Venta editada
                if previous_caja == self.caja:
                    # Caja no cambió → restar total anterior y sumar el nuevo
                    self.caja.total = self.caja.total - previous_total + self.total
                else:
                    # Caja cambió → restar de la caja anterior y sumar en la nueva
                    if previous_caja:
                        if previous_caja.total is None:
                            previous_caja.total = Decimal("0.00")
                        previous_caja.total -= previous_total
                        previous_caja.save(update_fields=['total'])
                    self.caja.total += self.total

            # Guardar total actualizado de la caja
            self.caja.save(update_fields=['total'])

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio

    def save(self, *args, **kwargs):
        # Si no se definió precio, usar el precio del producto
        if not self.precio and hasattr(self.producto, "precio"):
            self.precio = self.producto.precio
        super().save(*args, **kwargs)

        # 🔹 Actualizar el total de la venta asociada
        if self.sale_id:
            self.sale.save()

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"