from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
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

    def get(self, request, *args, **kwargs):
        try:
            expense = self.queryset.filter(user=request.user).all()
            return Response(ExpenseSerializer(expense, many=True).data)
        except Expense.DoesNotExist:
            return Response(
                data={
                    "message": "Expense does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )


    def post(self, request):
        try:
            try:
                expense = Expense.objects.create(
                    name=request.data["name"],
                    image=request.FILES["image"],
                    total=request.data["total"],
                    date=request.data["date"],
                    user=request.user
                )
            except:
                expense = Expense.objects.create(
                    name=request.data["name"],
                    total=request.data["total"],
                    date=request.data["date"],
                    user=request.user
                )
            return Response(
                data=ExpenseSerializer(expense).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({
                "message": str(e)
            })


class ExpenseView(generics.RetrieveUpdateDestroyAPIView):

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


    def delete(self, request, *args, **kwargs):
        try:
            expense = self.queryset.get(pk=kwargs["pk"])
            expense.delete()
            return Response(
                data={
                    'Deleted': True
                },
                status=status.HTTP_200_OK
            )
        except Expense.DoesNotExist:
            return Response(
                data={
                    "message": "Expense does not exit"
                },
                status=status.HTTP_404_NOT_FOUND
            )



class ExpenseGrandTotal(APIView):

    def  get(self, request, *args, **kwargs):
        expenses = Expense.objects.filter(user=request.user).all()
        sum_exp = 0
        for expense in expenses:
            sum_exp = sum_exp + expense.total
            return Response(
                data={
                    'grand_total': sum_exp
                },
                status=status.HTTP_200_OK
            )


class ExpenseSortView(APIView):


    def get(self, request, *args, **kwargs):
        sort_field = kwargs["pk"]
        expenses = []
        if sort_field == 1:
            expenses = Expense.objects.filter(user=request.user).order_by('-date').all()
        elif sort_field == 2:
            expenses = Expense.objects.filter(user=request.user).order_by('name').all()
        elif sort_field == 3:
            expenses = Expense.objects.filter(user=request.user).order_by('-total').all()
        else:
            return Response(
                data={
                    'error': "Seems like you called the wrong url",
                },
                status = status.HTTP_404_NOT_FOUND
            )
        return Response(ExpenseSerializer(expenses, many=True).data)


class ExpenseFilterView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            expenses = Expense.objects.filter(user=request.user).exclude(image='').all()
            return Response(ExpenseSerializer(expenses, many=True).data)

        except Exception as e:
            return Response(
                data={
                    "message": "Not Found or Something went wrong",
                },
                status=status.HTTP_404_NOT_FOUND
            )

class ExpenseSearchView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            query = request.GET["query"]
            expenses = Expense.objects.filter(name__icontains=query, user=request.user).all()
            return Response(ExpenseSerializer(expenses, many=True).data)

        except Exception as e:
            return Response(
                data={
                    "message": "Not Found or Something went wrong",
                },
                status=status.HTTP_404_NOT_FOUND
            )