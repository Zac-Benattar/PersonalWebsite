from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import pickle


def get_today_datetime():
    return timezone.now()

def get_in_hour_datetime():
    return timezone.now() + timezone.timedelta(hours=1)

def get_in_day_datetime():
    return timezone.now() + timezone.timedelta(days=1)

def get_in_week_datetime():
    return timezone.now() + timezone.timedelta(days=7)


class Project(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=3000, blank=True)
    client_name = models.CharField(max_length=50, blank=True)
    initial_budget = models.DecimalField(max_digits=15, decimal_places=2)
    current_budget = models.DecimalField(max_digits=15, decimal_places=2)
    amount_spent = models.DecimalField(max_digits=15, decimal_places=2)
    start_date = models.DateTimeField(default=get_today_datetime())
    initial_deadline = models.DateTimeField(default=get_in_week_datetime())
    current_deadline = models.DateTimeField(default=get_in_week_datetime())
    methodology = models.CharField(max_length=30)
    gitHub = models.CharField(max_length=150, blank=True)
    projectResult = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        '''Gets string representation of the project object
        Format: <project.name>

        Returns:
            str string representation of the project
        '''
        return self.name

    def get_members_count(self):
        '''Gets number of members of the project

        Returns:
            int number of members in the project
        '''
        return len(Member.objects.filter(project=self))

    def get_total_salary_expenses(self):
        '''Gets total salaries of the members of the project
        (1 year salary cost)

        Returns:
            decimal total of all members salaries
        '''
        if Member.objects.count() > 0:
            members = Member.objects.filter(project=self)
            salaries_total = 0
            for m in members:
                salaries_total += m.salary
            return salaries_total
        else:
            return 0

    def get_daily_running_cost(self):
        '''Gets average daily running cost of the project
        year salaries total / number of days running

        Returns:
            decimal average daily running cost of project
        '''
        days_running = (self.current_deadline - self.start_date).days
        if days_running != 0:
            return self.get_total_salary_expenses() / days_running
        else:
            return 0

    def has_no_feedback(self):
        '''Gets if the project has just started (true if project has no feedback yet)
        Ongoing project ML model cannot evaluate unless feedback exists in the project

        Returns:
            bool true if project has no feedback
        '''
        if Feedback.objects.count() > 0:
            feedbacks = Feedback.objects.filter(project=self)
            return len(feedbacks) == 0
        else:
            return True

    def get_average_happiness(self):
        '''Gets average happiness score of feedbacks for the project
        total happiness from feedbacks / no. feedbacks

        Returns:
            decimal average of feedback happiness values
        '''

        week_before = timezone.now() - timezone.timedelta(days=7)
        feedbacks = Feedback.objects.filter(project=self, date__gt=week_before)
        feedback_size = len(feedbacks)
        if feedback_size == 0:
            return 0
        else:
            total_happiness = 0
            for f in feedbacks:
                total_happiness += f.emotion
            return total_happiness / feedback_size

    def get_average_confidence(self):
        '''Gets average confidence score of feedbacks for the project
        total confidence from feedbacks / no. feedbacks

        Returns:
            decimal average of confidence happiness values
        '''
        week_before = timezone.now() - timezone.timedelta(days=7)
        feedbacks = Feedback.objects.filter(project=self, date__gt=week_before)
        feedback_size = len(feedbacks)
        if feedback_size == 0:
            return 0
        else:
            total_confidence = 0
            for f in feedbacks:
                total_confidence += f.confidence
            return total_confidence / feedback_size
        
    def get_completion(self):
        tasks = Task.objects.filter(project=self)
        
        if tasks.count() == 0:
            return 0
        
        total_completion = 0
        for t in tasks:
            total_completion += t.completion
            
        return total_completion / tasks.count()
    
    def get_start_date_unix(self):
        return int(self.start_date.timestamp())
    
    def get_initial_deadline_unix(self):
        return int(self.initial_deadline.timestamp())
    
    def get_current_deadline_unix(self):
        return int(self.current_deadline.timestamp())
        


class Skill(models.Model):
    # Please stop overwriting this with previous versions, name should NOT be the primary key
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        '''Gets string representation of the skill object
        Format: <skill.name>

        Returns:
            str string representation of the skill
        '''
        return self.name


class CustomUser(AbstractUser):
    # Using a library for phone number, if you want the string representation use phone.as_e164
    # https://django-phonenumber-field.readthedocs.io/en/latest/
    phone = PhoneNumberField(null=False, blank=True, unique=True)
    skillset = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        '''Gets string representation of the custom user object
        Format: <customuser.username>

        Returns:
            str string representation of the custom user
        '''
        return self.username


class RiskEvaluation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    success_chance = models.DecimalField(max_digits=13, decimal_places=10)
    date = models.DateTimeField(auto_now_add=True)
    initial_evaluation = models.BooleanField(default=True)
    serialized_project_evaluation_data = models.BinaryField(null=True)

    def __str__(self):
        '''Gets string representation of the time risk evaluation object
        Format: <riskevaluation.success_chance>

        Returns:
            str string representation of the risk evaluation
        '''
        return str(self.success_chance)

    def get_project_snapshot(self):
        result = pickle.loads(self.serialized_project_evaluation_data)
        return result
    
    def get_date_unix(self):
        return int(self.date.timestamp())


class Meeting(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    attendence = models.IntegerField(default=0)
    date = models.DateTimeField(default=get_in_week_datetime())
    duration = models.IntegerField(default=0)

    def __str__(self):
        '''Gets string representation of the time meeting object
        Format: <meeting.project.name> <meeting.date>

        Returns:
            str string representation of the meeting
        '''
        return self.project.__str__() + ' ' + self.date.__str__()


class Feedback(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    confidence = models.IntegerField(default=0)
    emotion = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Gets string representation of the time feedback object
        Format: <feedback.project.name> Feedback <feedback.pk>

        Returns:
            str string representation of the feedback
        '''
        return self.project.__str__() + ' Feedback ' + str(self.pk)


# This was originally allocated to a single member,
# instead I think multiple people should be able to
# participate in a task
class Task(models.Model):
    members = models.ManyToManyField('Member', blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True)
    duration = models.IntegerField(default=0)
    completion = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(default=get_in_hour_datetime())
    latest_finish = models.DateTimeField(default=get_in_week_datetime())
    dependent_tasks = models.ManyToManyField(
        'self', symmetrical=False, related_name='prerequisites', blank=True)
    NOTSTARTED = 'NS'
    STARTED = 'S'
    FINISHED = 'F'
    NOTAPPLICABLE = 'N/A'
    status_choices = [
        (NOTSTARTED, 'Not Started'),
        (STARTED, 'Started'),
        (FINISHED, 'Finished'),
        (NOTAPPLICABLE, 'Not Applicable'),
    ]
    completion_status = models.CharField(
        choices=status_choices,
        max_length=3,
        default='Not Applicable'
    )

    def __str__(self):
        '''Gets string representation of the task object
        Format: <task.name> <task.project.name>

        Returns:
            str string representation of the mask
        '''
        return self.name + ' ' + self.project.__str__()

    def get_duration(self):
        '''Gets the duration of the task by finding the difference
        between end_date and start_date. May be negative

        Returns:
            datetime.timedelta
        '''
        return self.latest_finish - self.start_date

    def creation_date_to_unix(self):
        return int(self.creation_date.timestamp())

    def start_date_to_unix(self):
        return int(self.start_date.timestamp())

    def earliest_finish_date_to_unix(self):
        earliest_finish = self.start_date + timezone.timedelta(days=self.duration)
        return int(earliest_finish.timestamp())

    def latest_finish_date_to_unix(self):
        return int(self.latest_finish.timestamp())
    
    def get_dependent_tasks_string(self):
        dependencies_list = self.dependent_tasks.all()
        dependencies_string = ''
        for t in dependencies_list:
            dependencies_string += str(t.id) + ','
        
        return dependencies_string



class Role(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Member(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    work_hours = models.IntegerField(default=0)
    join_date = models.DateTimeField(auto_now_add=True)
    project_manager = models.BooleanField(default=False)
    developer = models.BooleanField(default=True)
    salary = models.DecimalField(max_digits=15, decimal_places=2)
    has_quit = models.BooleanField(default=False)

    def __str__(self):
        '''Gets string representation of the task object
        Format: <member.user> <member.role> <member.project>

        Returns:
            str string representation of the member
        '''
        return self.user.__str__() + ' ' + self.role.__str__() + ' ' + self.project.__str__()


# Joins roles and skills
class RoleRequirement(models.Model):
    skillset = models.ManyToManyField(Skill)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        '''Gets string representation of the role requirement object
        Format: <rolerequirement.role>: <rolerequirementskill1>; <rolerequirementskill2>; ...

        Returns:
            str string representation of the role requirement
        '''
        output = self.role.__str__() + ': '
        for x in self.skillset.all():
            output = output+'; '+str(x)
        return output


# Used for tracking time worked
class TimeWorked(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    time = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        '''Gets string representation of the time worked object
        Format: <timeworked.member.name> <timeworked.task.name> <timeworked.time> hours

        Returns:
            str string representation of the timeworked
        '''
        return self.member.__str__() + ' ' + self.task.__str__() + ' ' + self.time.__str__() + ' hours'


class Suggestion(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    dismissed = models.BooleanField(default=False)

    def __str__(self):
        '''Gets string representation of the suggestion
        Format: <suggestion.name>

        Returns:
            str string representation of the suggestion
        '''
        return self.name
