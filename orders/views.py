from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Order, OrderItem
from .serializers import OrderSerializer
from menu.models import MenuItem
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
import json

logger = logging.getLogger(__name__)

# Template Views
class OrderList(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

# API Views
class OrderAPIList(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            # Create order
            order = Order.objects.create(
                user=request.user,
                special_instructions=request.data.get('special_instructions', ''),
                status='PLACED'
            )

            # Process items
            items_data = request.data.get('items', [])
            total_amount = 0

            for item in items_data:
                menu_item = MenuItem.objects.get(id=item['menu_item'])
                quantity = int(item['quantity'])
                price = menu_item.price * quantity
                
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity,
                    price=price
                )
                total_amount += price

            order.total_amount = total_amount
            order.save()

            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            if 'order' in locals():
                order.delete()
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class OrderAPIDetail(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def patch(self, request, *args, **kwargs):
        try:
            order = self.get_object()
            print(f"Updating order {order.id}")  # Debug print
            
            new_status = request.data.get('status')
            print(f"New status: {new_status}")  # Debug print
            
            # Allow users to cancel their own orders
            if new_status == 'CANCELLED':
                if order.user != request.user:
                    return Response(
                        {'detail': 'You can only cancel your own orders'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            else:
                # Only staff can update other statuses
                if not request.user.is_staff:
                    return Response(
                        {'detail': 'Only staff can update order status'},
                        status=status.HTTP_403_FORBIDDEN
                    )

            if new_status:
                if new_status not in dict(Order.STATUS_CHOICES):
                    return Response(
                        {'detail': 'Invalid status'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                old_status = order.status
                order.status = new_status
                order.save()
                
                print(f"Status updated from {old_status} to {new_status}")  # Debug print
                
                return Response({
                    'detail': f'Order status updated to {order.get_status_display()}',
                    'data': self.get_serializer(order).data
                })
            
            return Response(
                {'detail': 'Status not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            print(f"Error updating order: {str(e)}")  # Debug print
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class OrderStatusUpdate(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

# Add views for updating order status (if needed)

class StaffDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = 'orders/staff_dashboard.html'
    context_object_name = 'orders'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Order.objects.all().order_by('-created_at')

@login_required
@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["POST"])
def update_order_status(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        new_status = request.POST.get('status')
        
        if new_status not in dict(Order.STATUS_CHOICES):
            return JsonResponse({'error': 'Invalid status'}, status=400)
            
        order.status = new_status
        order.save()
        
        return JsonResponse({
            'message': f'Order #{pk} status updated to {order.get_status_display()}',
            'status': order.status,
            'status_display': order.get_status_display()
        })
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)