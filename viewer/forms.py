from django import forms

class SearchForm(forms.Form):
    year = forms.CharField(label='Choose a year', max_length=100,required=False)
    country = forms.CharField(label='Choose a country', max_length=100,required=False)
    institution = forms.CharField(label='Choose a institution', max_length=100,required=False)
    team_name = forms.CharField(label='Choose a team', max_length=100,required=False)
    medal = forms.CharField(label='Choose a medal',max_length=10,required=False)
    keyword = forms.CharField(label='Choose a keyword',max_length=20,required=False)
    awards = forms.BooleanField(required=False)
    nominations = forms.BooleanField(required=False)
    section = forms.ChoiceField(required=False, choices=(('',''),('overgrad','Overgrad'),('undergrad','Undergrad'),('highschool', 'High School')))