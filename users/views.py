from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserSerializerWithToken
from .permissions import IsNotAuthenticated


class UserCurrentView(APIView):

    permission_classes = (IsAuthenticated,)
    throttle_classes = (UserRateThrottle,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserCreateView(APIView):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsNotAuthenticated, )
    throttle_clasees = (AnonRateThrottle, ScopedRateThrottle,)
    throttle_scope = "register"

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

