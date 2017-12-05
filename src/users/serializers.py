from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import serializers

from users.models import Details


class DetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Details
        fields = ('country', 'goal', 'mobile_number')


class UserSerializer(serializers.ModelSerializer):

    details = DetailSerializer()

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 
            'email', 'username', 'last_login', 'date_joined', 'password', 
            'details'
        )
        read_only_fields = ('username', 'last_login','date_joined')
        extra_kwargs = {
            'password': { 'write_only': True }
        }

    def create(self, validated_data):
        details = validated_data.pop('details')
        new_user = User.objects.create_user(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            country=details.get('country'),
            goal=details.get('goal'),
            mobile_number=details.get('mobile_number'),
            password=validated_data.get('password')
        )

        return new_user
