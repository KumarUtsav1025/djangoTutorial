from rest_framework import serializers
from home.models import Person,Comapny
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('Username already taken')
            
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError('Email already taken')
            
        return data
    
    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model= Comapny
        fields = ['name']


class PersonSerializer(serializers.ModelSerializer):
    comapny = CompanySerializer()
    country = serializers.SerializerMethodField()


    class Meta:
        #depth=1
        model = Person
        fields = '__all__'

    def get_country(self, obj):
        company_obj = Comapny.objects.get(id = obj.comapny.id)
        return {'company name': company_obj.name, 'loacation': 'India'}

    def validate(self, data):
        if data['age'] < 18:
            raise serializers.ValidationError("Age should be graeter than 18.")
        return data