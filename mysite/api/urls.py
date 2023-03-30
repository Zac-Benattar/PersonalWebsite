from django.urls import path, include
from rest_framework_nested import routers
from api.views import * 
from rest_framework_simplejwt.views import TokenRefreshView


router = routers.DefaultRouter()
router.register(r'projects', ProjectsViewSet, basename='projects')
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'skills', SkillViewSet)

# add a specific project router


# project routers , api call : /api/projects/pk/model_name/pk
members_router = routers.NestedDefaultRouter( router, r'projects', lookup = 'project')
members_router.register( r'members', MemberViewSet, basename='project-members')

tasks_router = routers.NestedDefaultRouter( router, r'projects', lookup = 'project')
tasks_router.register( r'tasks', TaskViewSet, basename='project-tasks')

not_started_tasks_router = routers.NestedDefaultRouter( router, r'projects', lookup = 'project')
not_started_tasks_router.register( r'notstartedtasks', NotStartedTaskViewSet, basename='project-tasks-not-started')

started_tasks_router = routers.NestedDefaultRouter( router, r'projects', lookup = 'project')
started_tasks_router.register( r'startedtasks', StartedTaskViewSet, basename='project-tasks-started')

finished_tasks_router = routers.NestedDefaultRouter( router, r'projects', lookup = 'project')
finished_tasks_router.register( r'finishedtasks', FinishedTaskViewSet, basename='project-tasks-finished')

no_status_tasks_router = routers.NestedDefaultRouter( router, r'projects', lookup = 'project')
no_status_tasks_router.register( r'nostatustasks', NoStatusTaskViewSet, basename='project-tasks-no-status')

risk_evaluations_router = routers.NestedDefaultRouter( router, r'projects', lookup = 'project')
risk_evaluations_router.register( r'riskevaluations', RiskEvaluationViewSet, basename='project-riskEvaluations')

generate_risk_evaluation_router = routers.NestedDefaultRouter( router, r'projects', lookup = 'project')
generate_risk_evaluation_router.register( r'generateriskevaluation', RiskEvaluationGeneratorViewSet, basename='project-generateRiskEvaluation')

retrain_model_router = routers.NestedDefaultRouter( router, r'projects', lookup = 'project')
retrain_model_router.register( r'retrainmodel', RetrainView, basename='project-retrainmodel')

meetings_router = routers.NestedDefaultRouter( router, r'projects', lookup = 'project')
meetings_router.register( r'meetings', MeetingViewSet, basename='project-meetings')

feedback_router = routers.NestedDefaultRouter( router, r'projects', lookup = 'project')
feedback_router.register( r'feedback', FeedbackViewSet, basename='project-feedback')

suggestions_router = routers.NestedDefaultRouter( router, r'projects', lookup = 'project')
suggestions_router.register( r'suggestions', SuggestionViewSet, basename='project-suggestions')

generate_suggestions_router = routers.NestedDefaultRouter( router, r'projects', lookup = 'project')
generate_suggestions_router.register( r'generatesuggestions', SuggestionsGeneratorViewSet, basename='project-generateSuggestions')

# member routers , api call : /api/projects/pk/members/pk/model_name/pk
timeWorked_router = routers.NestedDefaultRouter( members_router, r'members', lookup = 'member')
timeWorked_router.register( r'timeworked', TimeWorkedViewSet, basename='member-timeWorked')

# role routers , api call : /api/roles/pk/model_name/pk
role_requirements_router = routers.NestedDefaultRouter(router, r'roles', lookup = 'role')
role_requirements_router.register(r'rolerequirements', RoleRequirementViewSet, basename = 'role-roleRequirements')

# user routers , api call : /api/users/pk/skill/pk
userSkills_router = routers.NestedDefaultRouter( router, r'users', lookup = 'user')
userSkills_router.register( r'skills', UserSkillViewSet, basename='user-userSkills')

# user routers , api call : /api/users/myaccount
userAccount_router = routers.NestedDefaultRouter( router, r'users', lookup = 'user')
userAccount_router.register( r'myaccount', MyAccountViewSet, basename='user-myAccount')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(userSkills_router.urls)),
    path('', include(role_requirements_router.urls)),
    path('', include(timeWorked_router.urls)),
    path('', include(members_router.urls)),
    path('', include(tasks_router.urls)),
    path('', include(not_started_tasks_router.urls)),
    path('', include(started_tasks_router.urls)),
    path('', include(finished_tasks_router.urls)),
    path('', include(no_status_tasks_router.urls)), 
    path('', include(risk_evaluations_router.urls)),
    path('', include(generate_risk_evaluation_router.urls)),
    path('', include(meetings_router.urls)),
    path('', include(feedback_router.urls)),
    path('', include(suggestions_router.urls)),
    path('', include(generate_suggestions_router.urls)),
    path('', include(userAccount_router.urls)),
    path('token/', MyTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('retrainmodel/<int:pk>/', RetrainView.as_view()),
]