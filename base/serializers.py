from rest_framework import serializers
from .models import * #imports all

class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class CourseSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
    