import unittest
import datetime

from django.test import TestCase
#from django.db import models
#from django.contrib.auth.models import User


from models import *

#from models import Project, Task, Member, Role, RoleRequirement, Feedback, User, Skill
from projectsuggester import ProjectSuggester


def test():
    print("Run test!")
    my_tester = tester()


class tester(unittest.TestCase):
    # CREATING A PROJECT
    name = "SE_project"
    description = "this project aims to ..."
    initial_budget = 40000
    current_budget = 3000
    initial_deadline = '2023-05-21 23:59:59'
    current_deadline = '2023-05-21 23:59:59'

    project1 = Project.objects.create(name, description, initial_budget, current_budget, initial_deadline, current_deadline)


    # CREATING A TASK
    name = "task 1"
    description = "description of task 1"
    duration = 30
    creation_date = datetime.date.today()
    completion_status = 'S'

    task1 = Task.objects.create(project1, name, description, duration, creation_date, completion_status)


    # CREATING FEEDBACK
    confidence = 5
    emotion = 5
    date = datetime.date.today()

    feedback1 = Feedback.objects.create(project1, confidence, emotion, date)


    # CREATING A ROLE
    name = "Project Manager"
    description = "The Project Manager is in charge of ..."

    role1 = Role.objects.create(name, description)


    # CREATING SKILLS
    name ="Leadership"
    description = "a good leader and able to inspire, motivate, and guide the team towards the project goals"
    skill1 = Skill.objects.create(name, description)

    name ="Communication"
    description = "Clear and effective communication skills. This includes written, verbal, and nonverbal communication"
    skill2 = Skill.objects.create(name, description)

    name ="Problem Solving"
    description = "excellent problem-solving skills to be able to identify issues and develop strategies to overcome them."
    skill3 = Skill.objects.create(name, description)

    name ="Planning and Organization"
    description = "be able to develop a project plan, including scheduling, resource allocation, and budgeting."
    skill4 = Skill.objects.create(name, description)

    name ="Team Management"
    description = " be able to manage a team effectively, including delegating tasks, resolving conflicts, and providing feedback."
    skill5 = Skill.objects.create(name, description)


    # CREATING ROLE REQUIREMENT
    PM = RoleRequirement.objects.create(role1)
    PM.skillset.add(skill1, skill2, skill3, skill4, skill5)


    # CREATING A USER
    username = "andrew.smith"
    forename = "Andrew"
    lastname = "Smith"
    join_date = '2023-01-01'
    email = 'andrew.smith74@gmail.com'
    phone = '+15555555555'

    user1 = CustomUser.objects.create(username, forename, lastname, join_date, email, phone)
    user1.skillset.add(skill1, skill2, skill3, skill4)


    # CREATING A MEMBER
    work_hours = 40

    member1 = Member.objects.create(role1, project1, user1, work_hours, user1.join_date)


    # CREATING FILEPATH OF A CODE
    file_path = r"C:\Users\alexp\Documents\GitHub\SoftwareProjectTracker\mysite\test\test.py"


    # TESTING

    # PAST DEADLINE FUNCTION
    ## function will return TRUE if the suggestion has to be displayed
    def test_past_deadline(self, project):
        test = ProjectSuggester(project)
        self.assertEqual(test.past_deadline(), True, 'The fuction is wrong.')

        if __name__ == '__main__':
            unittest.main()

    # CHANGING ROLES FUNCTION
    ## function will return TRUE if the suggestion has to be displayed
    def test_changing_roles(self, project):
        test = ProjectSuggester(project)
        self.assertEqual(test.changing_roles(), True, 'The fuction is wrong.')

        if __name__ == '__main__':
            unittest.main()

    # AVERAGE HAPPINESS FUNCTION
    ## function will return the average happiness
    def test_average_happiness(self, project):
        test = ProjectSuggester(project)
        self.assertEqual(test.average_happiness(), 5, 'The fuction is wrong.')

        if __name__ == '__main__':
            unittest.main()

    # COUNT COMMENTS FUNCTION
    ## function will return the number of comments
    def test_count_comments(self, file_path):
        test = ProjectSuggester(file_path)
        self.assertEqual(test.count_comments(), 1, 'The fuction is wrong.')

        if __name__ == '__main__':
            unittest.main()

    # COMPLETION RATIO FUNCTION
    ## function will return TRUE if the suggestion has to be displayed
    def test_completion_ratio(self, project):
        test = ProjectSuggester(project)
        self.assertEqual(test.changing_roles(), True, 'The fuction is wrong.')

        if __name__ == '__main__':
            unittest.main()

    # LOW BUDGET FUNCTION
    ## function will return TRUE if the suggestion has to be displayed
    def test_low_budget(self, project):
        test = ProjectSuggester(project)
        self.assertEqual(test.low_budget(), True, 'The fuction is wrong.')

        if __name__ == '__main__':
            unittest.main()
