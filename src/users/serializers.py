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

    def update(self, user_instance, validated_data):
        user_instance.first_name = validated_data.get('first_name')
        user_instance.last_name = validated_data.get('last_name')
        user_instance.email = validated_data.get('email')
        user_instance.set_username()
        
        details = validated_data.get('details')

        if details:
            try:
                detail_instance = Details.objects.get(user_id=user_instance.id)
                detail_instance.country = details.get('country')
                detail_instance.goal = details.get('goal')
                detail_instance.mobile_number = details.get('mobile_number')
                detail_instance.save()
            except Details.DoesNotExist:
                new_details = Details.objects.create(
                    user=user_instance,
                    country=details.get('country'),
                    goal=details.get('goal'),
                    mobile_number=details.get('mobile_number')
                )
                new_details.save()
        
        user_instance.save()

        return user_instance
        