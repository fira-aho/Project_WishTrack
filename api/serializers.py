from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from .models import User, WishlistItem, Transaction, SavingPlan, Reminder, Destination

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'first_name', 
            'last_name',
            'nick_name',
            'phone_number',
            'gender',
            'language'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        validate_password(attrs['password'])
        
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number')
        )
        
        user.set_password(validated_data['password'])
        user.save()
        
        return user

class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        read_only_fields = ['user', 'created_at', 'updated_at']
        fields = [
            'id', 
            'user', 
            'name', 
            'price', 
            'amount_saved', 
            'category', 
            'target_date', 
            'priority', 
            'image_url', 
            'description', 
            'product_link', 
            'status', 
            'created_at', 
            'updated_at'
        ]

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        read_only_fields = ['user', 'created_at']
        fields = '__all__'

class SavingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingPlan
        fields = '__all__'

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'

class WishlistProgressSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

class GoogleLoginSerializer(SocialLoginSerializer):
    access_token = serializers.CharField(required=True)

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'