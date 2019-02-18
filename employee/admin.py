from django.contrib import admin

# Register your models here.
from employee.models import Position,User


class PositionAdmin(admin.ModelAdmin):
	search_fields = ['name','description']
	list_filter = []
	list_display = ('name','description')
	fieldsets = [
		('Basic Information',{'fields': ['name','description']}),
	]
admin.site.register(Position,PositionAdmin)
# admin.site.register(User)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from models import CommonUser, Account, Registry
from django import forms


class MyUserChangeForm(UserChangeForm):
	class Meta(UserChangeForm.Meta):
		model = User


class MyUserCreationForm(UserCreationForm):
	# password = forms.CharField(
	#     label='Password',
	#     max_length = 32,
	#     required=True,
	#     widget=forms.PasswordInput,
	#     )

	# password2 = forms.CharField(
	#     label='Confirm',
	#     max_length = 32,
	#     required=True,
	#     widget=forms.PasswordInput,
	#     help_text="Make sure they match!",
	#     )

	password = ReadOnlyPasswordHashField(label= ("Password"),
		help_text= ("Raw passwords are not stored, so there is no way to see "
		"this user's password, but you can change the password "
		"using <a href=\"password/\">this form</a>."))


	class Meta(UserCreationForm.Meta):
		model = User
		fields = ['username', 'password', 'password2', 'email',
			'first_name','last_name']
		help_texts = {
			'password': 'Must be at least 8 characters.',
		}


	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError(self.error_messages['duplicate_username'])

class MyUserAdmin(UserAdmin):
	form 		= MyUserChangeForm
	add_form 	= MyUserCreationForm
	list_filter = ('company','section__department', 'section','position')
	list_display = ('username','first_name','last_name','en','position', 'section','company','is_staff')
	ordering = ['en','first_name']
	search_fields = ['username','first_name','last_name','en','email']
	set_unusable_password = None

	fieldsets 	= (
		('Personal info', {'fields': ('username','password',('title','first_name','last_name'),'en', 'email')}),
		('Department info', {'fields': ('company','section',('position'),'description')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
									   'groups', 'user_permissions',)}),
		('Important dates', {'fields': ('last_login', 'date_joined',)})
	)
	# +UserAdmin.fieldsets 

	add_fieldsets = (
		('Personal info', {
			'classes': ('wide',),
			'fields': ('username',('title','first_name', 'last_name'),'en',  'password1', 'password2', ),
		}),
		('Organize info', {
			'classes': ('wide',),
			'fields': ('company','section','position' ),
		})
	)

	


admin.site.register(User, MyUserAdmin)

