from rest_framework import viewsets,filters
from rest_framework import status, viewsets
from rest_framework.decorators import action,detail_route


from employee.models import User,Position
from employee.api.serializers import EmployeeSerializer,PositionSerializer




class EmployeeViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = EmployeeSerializer
	filter_backends = (filters.SearchFilter,)
	search_fields = ( 'first_name','last_name','en')

	@detail_route()
	def employees(self, request, pk=None):
		model = self.get_object()
		serializer = EmployeeSerializer(model.employees.all(), 
		context={'request': request}, many=True)
		return Response(serializer.data)

class PositionViewSet(viewsets.ModelViewSet):
	queryset = Position.objects.all()
	serializer_class = PositionSerializer
	filter_backends = (filters.SearchFilter,)
	search_fields = ('position_id', 'name', 'description')

	@detail_route()
	def employees(self, request, pk=None):
		position = self.get_object()
		serializer = EmployeeSerializer(position.employees.all(), 
		context={'request': request}, many=True)
		return Response(serializer.data)