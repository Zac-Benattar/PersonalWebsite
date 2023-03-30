from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import permissions, viewsets
from projects.models import *
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import NotFound
from rest_framework.decorators import permission_classes, action
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response

import sys #Import system file to add extra imports from outside file
import pathlib #Import the libary to modify paths

# Add the Risk_Assessment folder to the path
# Search path needs to be changed to find the files, later reverted
originalPath = sys.path
folderpath = str(pathlib.Path(__file__).parent.parent.joinpath('static\Risk_Assessment').resolve())
sys.path.append(folderpath)

#Import files to handle machine learning
from startevaluationdata import StartEvaluationData
from currentevaluationdata import CurrentEvaluationData
from projectevaluator import ProjectEvaluator
from projects.projectsuggester import ProjectSuggester

# Generate ProjectEvaluator and ProjectSuggester objects
# Used to get project evaluations and suggestions
PROJECT_EVALUATOR = ProjectEvaluator()
PROJECT_SUGGESTER = ProjectSuggester()

# Revert the import path to the original path
#  Might not be needed
sys.path = originalPath

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# read permissions for authenticated users
class IsOwnerOrCoWorker(permissions.BasePermission):
    message = 'Editing this field is restricted to the owners only'

    def has_object_permission(self, request, view, obj):
        # Only allow read permissions to members of the project
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow write permissions to members involved in the task
        if obj.members.filter(user_profile=request.user.id).exists():
            return True

        return False


class ProjectReadAndWritePermission(permissions.BasePermission):
    message = 'Editing projects is restricted to the project manager only'

    def has_object_permission(self, request, view, obj):
        # Only allow read permissions for members of the project
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only allow write permissions to project manager
        user = get_object_or_404(CustomUser, username=request.user)
        query_set = Member.objects.filter(
            user=user, project=obj.id, project_manager=True)
        if query_set.exists():
            return True

        return False


class ProjectsViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [ProjectReadAndWritePermission]

    def get_queryset(self):
        '''Gets list of projects that the logged in user is involved in

        Returns:
            list(projects)
        '''
        user_object = get_object_or_404(CustomUser, username=self.request.user)
        members = get_list_or_404(Member, user=user_object)
        queryset = None
        
        ids = list()
        for m in members:
            ids.append(m.project.id)
        queryset = Project.objects.filter(id__in=ids)
        
        return queryset


class MyAccountViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        '''Gets list of projects that the logged in user is involved in

        Returns:
            list(user)
        '''
        user = get_object_or_404(CustomUser, username=self.request.user)
        return user


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class UserSkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().prefetch_related(
        'customuser_set'
    ).all()

    serializer_class = SkillSerializer

    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs.get('user_pk')
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise NotFound('A user with this id does not exist')
        return self.queryset.filter(customuser=user)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class TimeWorkedViewSet(viewsets.ModelViewSet):
    queryset = TimeWorked.objects.all().select_related(
        'member'
    ).all()

    serializer_class = TimeWorkedSerializer

    def get_queryset(self, *args, **kwargs):
        member_id = self.kwargs.get("member_pk")
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            raise NotFound('A member with this id does not exist')
        return self.queryset.filter(member=member)


class RoleRequirementViewSet(viewsets.ModelViewSet):
    queryset = RoleRequirement.objects.all().select_related(
        'role'
    ).all()

    serializer_class = RoleRequirementSerializer

    def get_queryset(self, *args, **kwargs):
        role_id = self.kwargs.get("role_pk")
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            raise NotFound('A role with this id does not exist')
        return self.queryset.filter(role=role)


# select_related and prefetch_related are database function. select_related is used to select a single object ( Foreign Key ),
# prefetch_related gets back a set of things,
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().select_related(
        'project'
    ).all()

    serializer_class = MemberSerializer

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A project with this id does not exist')
        return self.queryset.filter(project=project)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related(
        'project'
    ).all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrCoWorker]

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A project with this id does not exist')
        return self.queryset.filter(project=project)


class NotStartedTaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related(
        'project'
    ).all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrCoWorker]

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A project with this id does not exist')
        return self.queryset.filter(project=project, completion_status='NS')


class StartedTaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related(
        'project'
    ).all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrCoWorker]

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A project with this id does not exist')
        return self.queryset.filter(project=project, completion_status='S')


class FinishedTaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related(
        'project'
    ).all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrCoWorker]

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A project with this id does not exist')
        return self.queryset.filter(project=project, completion_status='F')


class NoStatusTaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related(
        'project'
    ).all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrCoWorker]

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A project with this id does not exist')
        return self.queryset.filter(project=project, completion_status='N/A')


class RiskEvaluationViewSet(viewsets.ModelViewSet):
    queryset = RiskEvaluation.objects.all().select_related(
        'project'
    ).all()

    serializer_class = RiskEvaluationSerializer

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A project with this id does not exist')
        set = RiskEvaluation.objects.filter(project=project).order_by('-date')
        return set[0:1]


class RiskEvaluationGeneratorViewSet(viewsets.ModelViewSet):
    serializer_class = RiskEvaluationSerializer

    def generate_risk_evaluation(self, project):

        GENERATE_INITIAL_PREDICTION = project.has_no_feedback() #checks is the project has only just been started

        success_chance_estimate = 0 #Initialize success chance

        #Load in data
        initial_budget = float(project.initial_budget) #Cast from decimal to a float

        num_developers = len(Member.objects.filter(project = project, developer = True, has_quit = False)) #Get number of developers
        num_other_team_members = len(Member.objects.filter(project = project, developer = False, has_quit = False)) #Get number of team leaders etc.

        num_team_left = len(Member.objects.filter(project = project, has_quit = True)) #Get number of quit members

        original_deadline = project.initial_deadline #Get the deadline

        daily_running_cost = float(project.get_daily_running_cost()) #Get the running cost of the project

        num_tasks = len(Task.objects.filter(project = project)) #Get the number of tasks

        evaluation_data = None

        #Get chance of success
        # Initial prediction is for projects lacking tasks and feedback data from members.
        # It models projects that are still early on in the planning phase using less data points
        # The ongoing prediction provides a more accurate estimate due to it using more inputs
        if GENERATE_INITIAL_PREDICTION == True:
            print("==============================")
            print("GETTING AN INITIAL PREDICTION")
            print("")
            #Generate evaluation stats
            #initial_budget, num_developers, num_other_team_members, original_deadline, daily_running_cost, num_tasks
            start_evaluation_data = StartEvaluationData(
            initial_budget,
            num_developers,
            num_other_team_members,
            original_deadline,
            daily_running_cost,
            num_tasks)
            evaluation_data = start_evaluation_data

            #Evaluate data
            success_chance_estimate = PROJECT_EVALUATOR.get_initial_chance_of_success(start_evaluation_data)
        else:
            print("==============================")
            print("GETTING AN ONGOING PREDICTION")
            print("")
            #If the project is in progress add in extra stats
            #Load in more data
            current_budget = float(project.current_budget) #Cast from decimal to a float
            money_spent = float(project.amount_spent) #Cast from decimal to a float

            #Get project updated dealines
            #Get the current deadline (as well as the previously collected initial deadline)
            current_deadline = project.current_deadline

            #Get project finished tasks
            completed_tasks = len(Task.objects.filter(project = project, completion_status = 'F')) #Number of tasks finished

            #Get project developer stats
            average_happiness = float(project.get_average_happiness()) #The average happiness of developers
            average_confidence = float(project.get_average_confidence()) #The average confidence of the project from developers

            #Generate evaluation stats
            #initial_budget, current_budget, money_spent, num_developers, num_other_team_members, num_team_left, original_deadline, current_deadline, daily_running_cost, num_tasks, completed_tasks, average_happiness, average_confidence
            current_evaluation_data = CurrentEvaluationData(
            initial_budget,
            current_budget,
            money_spent,
            num_developers,
            num_other_team_members,
            num_team_left,
            original_deadline,
            current_deadline,
            daily_running_cost,
            num_tasks,
            completed_tasks,
            average_happiness,
            average_confidence)
            evaluation_data = current_evaluation_data
            
            print('data', current_evaluation_data)

            #Evaulate Data
            success_chance_estimate = PROJECT_EVALUATOR.get_current_chance_of_success(current_evaluation_data)

        pickled_date = pickle.dumps(evaluation_data)
        risk_evaluation = RiskEvaluation(project = project, success_chance = float(67.13273), serialized_project_evaluation_data=pickled_date)
        risk_evaluation.save()
        print('estimate', success_chance_estimate)
        return risk_evaluation

    def get_queryset(self, *args, **kwargs):

        project_id = self.kwargs.get("project_pk")

        try:
            project = Project.objects.get(id=project_id)
            risk_evaluation = self.generate_risk_evaluation(project)
        except Project.DoesNotExist:
            raise NotFound('A project with this id does not exist')
        return (risk_evaluation),


class RetrainView(APIView):
    def get(self, request, pk):

        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        risk_evaluations = RiskEvaluation.objects.filter(project=project)

        project_start_evaluation_data = None

        all_past_inprogress_evaluation_data = list()

        # Get the initial project evaluation data and a list of all subsiquent data
        for r in risk_evaluations:
            evaluation_data = r.get_project_snapshot()
            if evaluation_data.is_start_evaluation_data():
                project_start_evaluation_data = evaluation_data
            if evaluation_data.is_current_evaluation_data():
                all_past_inprogress_evaluation_data.append(evaluation_data)

        result = -1
        if project.projectResult == 'S':
            result = 1

        PROJECT_EVALUATOR.update_model(project_start_evaluation_data, all_past_inprogress_evaluation_data, result)

        context = {
            'result' : 'success'
        }
        return Response(context)


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all().select_related(
        'project'
    ).all()

    serializer_class = MeetingSerializer

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A project with this id does not exist')
        return self.queryset.filter(project=project)


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all().select_related(
        'project'
    ).all()

    serializer_class = FeedbackSerializer

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A project with this id does not exist')
        return self.queryset.filter(project=project)


class SuggestionViewSet(viewsets.ModelViewSet):
    queryset = Suggestion.objects.all().select_related(
        'project'
    ).all()

    serializer_class = SuggestionSerializer

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A project with this id does not exist')
        return self.queryset.filter(project=project, dismissed=False)


class SuggestionsGeneratorViewSet(viewsets.ModelViewSet):
    serializer_class = SuggestionSerializer

    def generate_suggestions(self, thing, project):
        return PROJECT_SUGGESTER.get_suggestions(project)

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
            suggestions = self.generate_suggestions(self, project)
        except Project.DoesNotExist:
            raise NotFound('A project with this id does not exist')
        return suggestions
