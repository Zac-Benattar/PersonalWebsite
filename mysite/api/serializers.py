#converts python model objects to json inkedId
from rest_framework.serializers import ModelSerializer, IntegerField, CharField
from projects.models import * 

class ProjectSerializer(ModelSerializer):
    completion = IntegerField(source='get_completion')
    start_date_unix = IntegerField(source='get_start_date_unix')
    initial_deadline_unix = IntegerField(source='get_initial_deadline_unix')
    current_deadline_unix = IntegerField(source='get_current_deadline_unix')
    class Meta:
        model = Project
        exclude = ('start_date', 'initial_deadline', 'current_deadline')
        read_only_fields = ('completion', 'start_date_unix', 'initial_deadline_unix', 'current_deadline_unix')

class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class RoleRequirementSerializer(ModelSerializer):
    class Meta:
        model = RoleRequirement
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields ='__all__'
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

    def create(self, validated_data):
        get_user = self.context['request'].user
        skill = super().create(validated_data)
        get_user.skillset.add(skill)
        get_user.save()
        return skill

class MemberSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class TimeWorkedSerializer(ModelSerializer):
    class Meta:
        model = TimeWorked
        fields = '__all__'

class RiskEvaluationSerializer(ModelSerializer):
    date_unix = IntegerField(source='get_date_unix')
    class Meta:
        model = RiskEvaluation
        read_only_fields = ('date_unix',)
        exclude = ('date',)

class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class SuggestionSerializer(ModelSerializer):
    class Meta:
        model = Suggestion
        fields = '__all__'

class MeetingSerializer(ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'
        
class TaskSerializer(ModelSerializer):
    creation_date_unix = IntegerField(source='creation_date_to_unix')
    start_date_unix = IntegerField(source='start_date_to_unix')    
    earliest_finish_date_unix = IntegerField(source='earliest_finish_date_to_unix')
    latest_finish_date_unix = IntegerField(source='latest_finish_date_to_unix')
    dependent_tasks_string = CharField(source='get_dependent_tasks_string')
    
    class Meta:
        model = Task
        exclude = ('creation_date', 'start_date', 'latest_finish')
        read_only_fields = ('creation_date_unix', 'start_date_unix', 'earliest_finish_date_unix', 'latest_finish_date_unix', 'dependent_tasks_string')