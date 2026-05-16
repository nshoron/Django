from django.contrib import admin
from .models import Category, Brand, Size, Color, Product, ProductVariant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ["name", "color_code"]
    search_fields = ["name"]
    ordering = ["name"]


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ["product_code", "size", "color"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "brand"]
    list_filter = ["category", "brand"]
    search_fields = ["name"]
    inlines = [ProductVariantInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ["product_code", "product", "size", "color"]
    list_filter = ["product", "size", "color"]
    search_fields = ["product_code", "product__name"]