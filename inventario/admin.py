from django.contrib import admin
from .models import Producto, Categoria, Cliente, Sale, SaleItem

# Admin para Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'categoria', 'cantidad', 'precio_compra', 'precio_venta', 'ganancia')
    search_fields = ('nombre', 'marca')
    list_filter = ('categoria',)

# Admin para Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# Admin para Cliente
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'documento')
    search_fields = ('nombre', 'documento')

# Inline para los items de la venta (defínelo ANTES de usarlo en SaleAdmin)
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

# Admin para Sale
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'tipo_comprobante', 'fecha', 'total_venta')
    list_filter = ('tipo_comprobante', 'fecha')
    search_fields = ('cliente',)
    inlines = [SaleItemInline]  # ahora sí funciona

    def total_venta(self, obj):
        return sum(item.quantity * item.price for item in obj.saleitem_set.all())
    total_venta.short_description = "Total Venta"

# Admin para SaleItem (opcional)
@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'producto', 'cantidad', 'precio')
    search_fields = ('product__nombre',)
    
    def subtotal(self, obj):
        return obj.quantity * obj.price
    subtotal.short_description = "Subtotal"
