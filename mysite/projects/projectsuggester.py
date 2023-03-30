import datetime
from .models import *

# retrieve all instances
all_projects = Project.objects.all()
all_tasks = Task.objects.all()
all_members = Member.objects.all()
all_roles = Role.objects.all()
all_rolerequirements = RoleRequirement.objects.all()
all_feedback = Feedback.objects.all()

generated_suggestions = list()

class ProjectSuggester:  # evaluating project's parameters to make suggestions

    def __init__(self):
        pass

    def get_suggestions(self, project):
        self.tasks_past_deadline(project)
        self.low_average_happiness(project)
        self.low_budget(project)
        self.low_completion_ratio(project)
        self.missing_skillsets(project)
        return generated_suggestions

    def tasks_past_deadline(self, project):
        # For all uncompleted tasks, If currentDate > taskDeadline.
        # The program will suggest allocating more people to that task.

        task_past_deadline = False

        # iterate over the tasks in the project that are uncompleted
        for task in all_tasks:
            if task.project == project:
                if task.completion_status != 'F':
                    if datetime.datetime.now(timezone.utc) > (task.creation_date + datetime.timedelta(hours=task.duration)):
                        description = (f"You've run out of time to complete the task {task.name}.\
                                Try allocating more people to the task.")

                        suggestion = Suggestion(
                            project=project,
                            name='Task past deadline',
                            description=description
                        )

                        # Save suggestion to the database
                        suggestion.save()
                        # Record suggestion to the of generated suggestions
                        generated_suggestions.append(suggestion)
                        task_past_deadline = True

        return task_past_deadline

    def missing_skillsets(self, project):
        # For all member of a project if any are assigned a role for which they don’t have
        # all the skills.
        # The program will suggest changing their role.

        roles_not_statisfied = False

        # iterate over all the memebers in the project
        for member in all_members:
            if member.project == project:
                for rolereq in all_rolerequirements:
                    if member.role == rolereq.role:
                        if rolereq.skillset != member.user.skillset:
                            description = (f"Member {member.user.get_username()} doesn't have the required skills \
                                for the role as {member.role.name} in the project {project.name}.\
                                    Try changing their role to one more adequate.")

                            suggestion = Suggestion(
                                project=project,
                                name='User skills missing',
                                description=description
                            )

                            # Save suggestion to the database
                            suggestion.save()
                            # Record suggestion to the of generated suggestions
                            generated_suggestions.append(suggestion)
                            roles_not_statisfied = True

        return roles_not_statisfied

    def low_average_happiness(self, project):
        # Looking at the mean average of happiness if below a certain threshold
        # The program will warn the project manager team happiness is low.
        
        if all_feedback.count() == 0:
            return False

        avg_happiness = 0
        count = 0
        
        for f in all_feedback:
            if f.project == project:
                avg_happiness += f.emotion
                count += 1

        if count > 0:
            avg_happiness = avg_happiness / count
        
        happiness_low = False

        if avg_happiness <= 2.5:  # half of the max happiness value
            description = (f"The average happiness of the members of the project {project.name} \
                    is low: {avg_happiness}.")

            suggestion = Suggestion(
                project=project,
                name='Low average happiness',
                description=description
            )

            # Save suggestion to the database
            suggestion.save()
            # Record suggestion to the of generated suggestions
            generated_suggestions.append(suggestion)
            happiness_low = True

        return happiness_low

    def count_comments(self, file_path, project):
        # Counting the comments of a python file
        # The program will suggest adding code comments to the file in question.
        
        low_comments = False

        with open(file_path, "r") as file:
            lines = file.readlines()

            line_count = len(lines)

            comment_count = 0
            for line in lines:
                line = line.strip()
                if line.startswith("#"):
                    comment_count += 1

        if comment_count < line_count / 6:
            description = (f"You may want to consider adding more comments to the file {file_path} \
                    to make it more understandable.")
            suggestion = Suggestion(
                project=project,
                name='Low average happiness',
                description=description
            )

            # Save suggestion to the database
            suggestion.save()
            # Record suggestion to the of generated suggestions
            generated_suggestions.append(suggestion)
            low_comments = True
            
        return low_comments

    def low_completion_ratio(self, project):
        # The program will calculate two values. The ratio of tasks completed.
        # And also a ratio of the time used from the start date to the current deadline.
        # If the time ratio is much higher than the task completion ratio it implies the
        # project may not be completed in time.
        # The program will suggest extending the deadline.

        task_count = 0
        for task in all_tasks:
            if task.project == project:
                task_count += 1

        completed_task_count = 0
        for task in all_tasks:
            if task.project == project:
                if task.completion_status == 'F':
                    completed_task_count += 1

        tasks_ratio = completed_task_count / task_count
        time_ratio = (datetime.datetime.now(timezone.utc) - project.start_date).total_seconds() / \
            (project.current_deadline - project.start_date).total_seconds()

        low_completion_ratio = False    

        if time_ratio < tasks_ratio:
            description = (f"We suggest extending the deadline for the project {project.name} to \
                    complete the remaining taks.")
            
            suggestion = Suggestion(
                project=project,
                name='Low average task completion rate',
                description=description
            )

            # Save suggestion to the database
            suggestion.save()
            # Record suggestion to the of generated suggestions
            generated_suggestions.append(suggestion)
            low_completion_ratio = True

        return low_completion_ratio

    def low_budget(self, project):
        # The program will create an estimation of a per day running cost. By summing
        # a daily salary and calculating how much money is left.
        # The program will suggest increasing the budget.

        budget_ratio = project.current_budget / project.initial_budget
        time_ratio = (project.current_deadline - project.start_date).total_seconds() / \
            (project.current_deadline - project.start_date).total_seconds()
        
        low_budget = False

        if time_ratio > budget_ratio:
            description = (f"We suggest increasing the budget for the project {project.name} to \
                    complete the remaining taks.")
            
            suggestion = Suggestion(
                project=project,
                name='Low budget',
                description=description
            )

            # Save suggestion to the database
            suggestion.save()
            # Record suggestion to the of generated suggestions
            generated_suggestions.append(suggestion)
            low_budget = True

        return low_budget
