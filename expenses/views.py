from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExpenseSerializer
from .models import Expense


class ExpenseCreateView(generics.ListCreateAPIView):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def post(self, request):
        try:
            try:
                expense = Expense.objects.create(
                    name=request.data["name"],
                    image=request.FILES["image"],
                    total=request.data["total"],
                    date=request.data["date"]
                )
            except:
                expense = Expense.objects.create(
                    name=request.data["name"],
                    total=request.data["total"],
                    date=request.data["date"]
                )
            return Response(
                data=ExpenseSerializer(expense).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({
                "message": str(e)
            })


class ExpenseView(generics.RetrieveUpdateAPIView):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get(self, request, *args, **kwargs):
        try:
            expense = self.queryset.get(pk=kwargs["pk"])
            return Response(ExpenseSerializer(expense).data)
        except Expense.DoesNotExist:
            return Response(
                data={
                    "message": "Expense does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            expense = self.queryset.get(pk=kwargs["pk"])
            serializer = ExpenseSerializer()
            updated_expense = serializer.update(expense, request.data)
            return Response(ExpenseSerializer(updated_expense).data)
        except Expense.DoesNotExist:
            return Response(
                data={
                    "message": "Expense does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )


