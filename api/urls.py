from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'wishlist-items', views.WishlistItemViewSet, basename='wishlistitem')
router.register(r'transactions', views.TransactionViewSet, basename='transaction')
router.register(r'saving-plans', views.SavingPlanViewSet, basename='savingplan')
router.register(r'reminders', views.ReminderViewSet, basename='reminder')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('financial-summary/', views.FinancialSummaryView.as_view(), name='financial_summary'),
]