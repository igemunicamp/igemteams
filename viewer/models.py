from django.db import models

# Create your models here.

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

	def __str__(self):
		return self.team_name + str(self.year)

