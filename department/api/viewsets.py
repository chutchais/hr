from rest_framework import viewsets,filters
from rest_framework import status, viewsets
from rest_framework.decorators import action,detail_route
from rest_framework.response import Response

from department.models import Department,Section
from employee.models import Employee
from department.api.serializers import DepartmentSerializer,SectionSerializer
from employee.api.serializers import EmployeeSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
	queryset = Department.objects.all()
	serializer_class = DepartmentSerializer
	filter_backends = (filters.SearchFilter,)
	search_fields = ('department_id', 'name', 'description')

	@detail_route()
	def sections(self, request, pk=None):
		department = self.get_object()
		serializer = SectionSerializer(department.sections.all(), 
			context={'request': request}, many=True)
		return Response(serializer.data)

	@detail_route()
	def employees(self, request, pk=None):
		model = self.get_object()
		serializer = EmployeeSerializer(Employee.objects.filter(
										section__in = Section.objects.filter(department=model)
										), 
			context={'request': request}, many=True)
		return Response(serializer.data)

class SectionViewSet(viewsets.ModelViewSet):
	queryset = Section.objects.all()
	serializer_class = SectionSerializer
	filter_backends = (filters.SearchFilter,)
	search_fields = ('section_id', 'name', 'description','departmrnt')

	@detail_route()
	def employees(self, request, pk=None):
		model = self.get_object()
		serializer = EmployeeSerializer(model.employees.all(), 
			context={'request': request}, many=True)
		return Response(serializer.data)