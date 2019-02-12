# from rest_framework import serializers
# # from django.contrib.auth.models import User
# from employee.models import User,Position


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email')

# class EmployeeSerializer(serializers.ModelSerializer):
# 	user = UserSerializer(required=True)
# 	class Meta:
# 		model = User
# 		fields = ['user','title','en',
# 				'name_thai','description','company',
# 				'section','position','role','manager','url']

# class PositionSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Position
# 		fields = ['position_id','name','description','url']