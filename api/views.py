from rest_framework import viewsets, permissions, generics, views, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from .models import User, WishlistItem, Transaction, SavingPlan, Reminder, Destination
from .serializers import UserSerializer, WishlistItemSerializer, RegisterSerializer, TransactionSerializer, SavingPlanSerializer, ReminderSerializer, WishlistProgressSerializer, GoogleLoginSerializer, DestinationSerializer

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully. Now perform Login to get your token."
        })

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class WishlistItemViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='add-progress')
    def add_progress(self, request, pk=None):
        wishlist_item = self.get_object()
        
        if wishlist_item.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        progress_serializer = WishlistProgressSerializer(data=request.data)
        if progress_serializer.is_valid():
            amount_to_add = progress_serializer.validated_data['amount']
            
            wishlist_item.amount_saved = F('amount_saved') + amount_to_add
            wishlist_item.save()
            wishlist_item.refresh_from_db()

            if wishlist_item.amount_saved >= wishlist_item.price:
                wishlist_item.status = 'COMPLETED'
                wishlist_item.save()

            return Response(WishlistItemSerializer(wishlist_item).data)
        else:
            return Response(progress_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FinancialSummaryView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        
        total_income = Transaction.objects.filter(
            user=user, type='INCOME'
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_expenses = Transaction.objects.filter(
            user=user, type='EXPENSE'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        balance = total_income - total_expenses
        
        return Response({
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': balance
        })

class SavingPlanViewSet(viewsets.ModelViewSet):
    serializer_class = SavingPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavingPlan.objects.filter(wishlist_item__user=self.request.user)

class ReminderViewSet(viewsets.ModelViewSet):
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(saving_plan__wishlist_item__user=self.request.user)

class WishMatchRecommendationView(generics.ListAPIView):
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        latest_item = WishlistItem.objects.filter(user=user).order_by('-created_at').first()
        
        if not latest_item or not latest_item.category:
            return WishlistItem.objects.none()

        target_category = latest_item.category
        
        recommendations = WishlistItem.objects.filter(
            category=target_category
        ).exclude(
            user=user
        ).order_by('-created_at')[:10]
        
        return recommendations

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = GoogleLoginSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

class DestinationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [permissions.AllowAny]