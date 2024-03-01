from rest_framework import serializers
from .models import User,UserAddress,Country,City,State


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    county = CountrySerializer()
    class Meta:
        model = State
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    state = StateSerializer()
    class Meta:
        model = City
        fields = '__all__'

class UserAddressSerializer(serializers.ModelSerializer):
    locality = CitySerializer()
    class Meta:
        model = UserAddress
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label="Password Confirmation")

    class Meta:
        model = User
        fields = ['first_name','last_name','email','password','password2','mobile_no']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        del attrs['password2']
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password','last_login','is_active','is_staff','is_superuser']






