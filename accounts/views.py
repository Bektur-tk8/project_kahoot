from accounts.models import User
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer, UsersListSerializer
from knox.models import AuthToken
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.generics import ListAPIView


class LoginAPI(generics.GenericAPIView):
	serializer_class = LoginSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data

		return Response({
			'user': UserSerializer(user).data,
			'token': AuthToken.objects.create(user)[1]
		})


class RegisterAPI(generics.GenericAPIView):
	serializer_class = RegisterSerializer

	def post(self, request, *args, **kwargs):
		print(request.data)
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()


		return Response({
			'user': UserSerializer(user).data,
			'token': AuthToken.objects.create(user)[1]
		})


class UserAPI(generics.RetrieveAPIView):
	permission_classes = [
		permissions.IsAuthenticated
	]
	serializer_class = UserSerializer

	def get_object(self):
		self.request.user


class UsersListView(ListAPIView):
	queryset = User.objects.all().order_by('-score')
	serializer_class = UsersListSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['name', 'second_name', 'phone_number']
	filterset_fields = ['group']