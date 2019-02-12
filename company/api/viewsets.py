# from rest_framework import viewsets,filters
# from rest_framework import status, viewsets
# from rest_framework.decorators import action,detail_route
# from rest_framework.response import Response


# from company.models import Company
# from company.api.serializers import CompanySerializer
# from employee.api.serializers import EmployeeSerializer

# class CompanyViewSet(viewsets.ModelViewSet):
# 	queryset = Company.objects.all()
# 	serializer_class = CompanySerializer
# 	filter_backends = (filters.SearchFilter,)
# 	search_fields = ( 'name', 'description')

# 	@detail_route()
# 	def employees(self, request, pk=None):
# 		company = self.get_object()
# 		serializer = EmployeeSerializer(company.employees.all(), 
# 		context={'request': request}, many=True)
# 		return Response(serializer.data)

# 	# def partial_update(self, request, pk=None):
# 	# 	print ('partial - update')
# 	# 	instance = self.get_object()
# 	# 	serializer = CompanySerializer(instance, data=request.data, partial=True)
# 	# 	# serializer.is_valid(raise_exception=True)
# 	# 	new_instance = serializer.save()
# 	# 	return Response(serializer.data)

# 	# @action(methods=['post'], detail=True)
# 	# def set_title(self, request, pk=None):
# 	# 	company = self.get_object()
# 	# 	serializer = CompanySerializer(company,data=request.data,partial=True)
# 	# 	if serializer.is_valid():
# 	# 		company.description = serializer.data['description']
# 	# 		company.save()
# 	# 		return Response({'status': 'title set'})
# 	# 	else:
# 	# 		return Response(serializer.errors,
# 	# 						status=status.HTTP_400_BAD_REQUEST)

# 	# @action(detail=False)
# 	# def recent_users(self, request):
# 	#     recent_users = User.objects.all().order('-last_login')

# 	#     page = self.paginate_queryset(recent_users)
# 	#     if page is not None:
# 	#         serializer = self.get_serializer(page, many=True)
# 	#         return self.get_paginated_response(serializer.data)

# 	#     serializer = self.get_serializer(recent_users, many=True)
# 	#     return Response(serializer.data)
# 	# def get_permissions(self):
# 	   #  """
# 	   #  Instantiates and returns the list of permissions that this view requires.
# 	   #  """
# 	   #  if self.action == 'list':
# 	   #      permission_classes = [IsAuthenticated]
# 	   #  else:
# 	   #      permission_classes = [IsAdmin]
# 	   #  return [permission() for permission in permission_classes]