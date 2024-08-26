from category.serializers import *
from goal.models import Goal


class GoalSerializer(serializers.ModelSerializer):
    category = SubCategorySerializer(read_only=True)

    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'amount', 'completed', 'start_date', 'due_date', 'updated_at',
                  'category', ]
