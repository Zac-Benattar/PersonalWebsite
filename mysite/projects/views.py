from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.views import View
from django.utils import timezone

from .models import *

# from static.Risk_Assessment.projectevaluator import ProjectEvaluator

class IndexView(View):
    def get(self, request):
        """Returns HttpResponse containing index page listing all projects that are in progress

        Returns:
            HttpResponse: index.html with context: projects
        """
        projects = Project.objects.filter(current_deadline__gte=timezone.now()).order_by('-current_deadline')[:]
        context = {'projects':projects}
        return render(request, 'projects/index.html', context)


class DetailView(View):    
    def get(self, request, pk):
        """Returns HttpResponse containing detail page listing:
        The relevant project's details
        The relevant project's risk evaluation

        Returns:
            HttpResponse: detail.html with context: project, riskevaluation
        """
        
        # evaluator = ProjectEvaluator()
        # evaluator.update_model()

        # Here we should load the model, calculate the risk score, create a new risk evaluation,
        # save the risk evaluation and send it to the page.
        # It may be neccesary to limit how often the user can calculate a new score, so maybe if there is a recent
        # enough evaluation e.g. within the last 5 mins we don't recalculate
        
        context = {
            'project' : get_object_or_404(Project, pk=self.kwargs['pk']),
            'riskevaluation' : RiskEvaluation.objects.filter(project=get_object_or_404(Project, pk=self.kwargs['pk'])).order_by('-date').last()
        }
        return render(request, 'projects/detail.html', context)


class PeopleView(View):
    def get(self, request, pk):
        """Returns HttpResponse containing people page listing:
        The relevant project's basic details
        The people involved with the project's basic details

        Returns:
            HttpResponse: people.html with context: project, members
        """
        context = {
            'project' : get_object_or_404(Project, pk=self.kwargs['pk']),
            'members' : Member.objects.filter(project=get_object_or_404(Project, pk=self.kwargs['pk'])).order_by('-join_date')
        }
        return render(request, 'projects/people.html', context)


class TasksView(View):    
    def get(self, request, pk):
        """Returns HttpResponse containing tasks page listing:
        The relevant project's basic details
        The tasks associated with the project
        The number of tasks associated

        Returns:
            HttpResponse: tasks.html with context: project, tasks, tasksCount
        """
        tasks = Task.objects.filter(project=get_object_or_404(Project, pk=self.kwargs['pk'])).order_by('-creation_date')
        context = {
            'project' : get_object_or_404(Project, pk=self.kwargs['pk']),
            'tasks' : tasks,
            'tasks_count' : str(len(tasks))
        }
        return render(request, 'projects/tasks.html', context)



class SuggestionsView(View):
    def get(self, request, pk):
        """Returns HttpResponse containing recommendations page listing:
        The relevant project's basic details
        The relevant project's recommendations
        The number of recommendations for the project

        Returns:
            HttpResponse: detail.html with context: project, recommendations, recommendations_count
        """
        recommendations = Suggestion.objects.filter(project=get_object_or_404(Project, pk=self.kwargs['pk'])).order_by('-creation_date')
        context = {
            'project' : get_object_or_404(Project, pk=self.kwargs['pk']),
            'recommendations' : recommendations,
            'recommendations_count' : str(len(recommendations))
        }
        return render(request, 'projects/suggestions.html', context)

