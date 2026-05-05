from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet

from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer


class CartViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    lookup_value_regex = r'me|[0-9]+'

    def get_queryset(self):
        return Cart.objects.prefetch_related(
            Prefetch('items', queryset=CartItem.objects.select_related('product_variant')),
        )

    def get_object(self):
        lookup = str(self.kwargs['pk'])
        qs = self.get_queryset()
        if lookup == 'me':
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
            return qs.get(pk=cart.pk)
        return get_object_or_404(qs, pk=lookup, user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user).select_related('cart')

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        variant = serializer.validated_data['product_variant']
        existing = CartItem.objects.filter(cart=cart, product_variant=variant).first()
        if existing:
            qty = serializer.validated_data.get('quantity', 1)
            existing.quantity += qty
            existing.save(update_fields=['quantity'])
            serializer.instance = existing
            return
        serializer.save(cart=cart)
