import csv

from viewer.models import Project

with open('igemteams.csv', newline='') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
		projectInst = Project(year = row['Year'], team_name = row['Team Name'], wiki = row['Wiki'], location = row['Location'], institution = row['Institution'],section = row['Section'],project_title = row['Project Title'], track = row['Track'],abstract = row['Abstract'], parts = row['Parts'],medal = row['Medal'],nominations = row['Nominations'],awards = row['Awards'])
		projectInst.save()


class Project(models.Model):
	year = models.PositiveSmallIntegerField(default=0)
	team_name = models.CharField(max_length=200)
	wiki = models.URLField(max_length=200)
	location = models.CharField(max_length=200)
	institution = models.CharField(max_length=200)
	section = models.CharField(max_length=200)
	project_title = models.CharField(max_length=200)
	track = models.CharField(max_length=200)
	abstract = models.TextField()
	parts = models.URLField(max_length=200)
	medal = models.CharField(max_length=200)
	nominations = models.CharField(max_length=200)
	awards = models.CharField(max_length=200)









