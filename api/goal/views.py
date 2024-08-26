from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from category.models import SubCategory
from goal.models import Goal
from goal.serializers import GoalSerializer


class GoalListApiView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        goals = Goal.objects.filter(user=request.user)
        serializer = GoalSerializer(goals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        category = request.data.get('category')
        sub_category = SubCategory.objects.filter(name__icontains=category)
        category_id = sub_category.first().id if sub_category.exists() else None
        data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'amount': request.data.get('amount'),
            'completed': request.data.get('completed'),
            'category': category_id,
            'start_date': request.data.get('start_date'),
            'due_date': request.data.get('due_date'),
            'user_id': request.user.id
        }

        serializer = GoalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoalDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        goal = Goal.objects.get(id=pk, user=request.user)

        serializer = GoalSerializer(goal.first())
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        try:
            goal = Goal.objects.get(id=pk, user=request.user)
        except Goal.DoesNotExist:
            return Response({'error': 'Goal not found'}, status=status.HTTP_404_NOT_FOUND)
        data = {
            'category': request.data.get('category', goal.category),
            'description': request.data.get('description', goal.description),
            'completed': request.data.get('completed', goal.completed),
            'user': request.user
        }
        serializer = GoalSerializer(goal, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            goal = Goal.objects.get(id=pk, user=request.user)
        except Goal.DoesNotExist:
            return Response({'error': 'Goal not found'}, status=status.HTTP_404_NOT_FOUND)
        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
