from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class WaterForm(forms.Form):
    action = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='flat_form')
    water_hardness = forms.FloatField(min_value=0, max_value=9, step_size=0.1)
    water_iron = forms.FloatField(min_value=0, max_value=9, step_size=0.1)
    water_turbidity = forms.FloatField(min_value=0, max_value=9, step_size=0.1)
    water_PH = forms.FloatField(min_value=0, max_value=9, step_size=0.1)
    water_oxid = forms.FloatField(min_value=0, max_value=9, step_size=0.1)
    water_nitrat = forms.FloatField(min_value=0, max_value=9, step_size=0.1)
    water_salt = forms.FloatField(min_value=0, max_value=9, step_size=0.1)
    water_nitrit = forms.FloatField(min_value=0, max_value=9, step_size=0.1)
    water_color = forms.FloatField(min_value=0, max_value=9, step_size=0.1)
    water_smell = forms.NullBooleanField(widget=forms.RadioSelect(
        choices=[
            (True, 'Да'),
            (False, 'Нет'),
        ]
    ))

class HouseForm(WaterForm):
    action = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='house_form')
    people_number = forms.IntegerField(min_value=0)

class ContryForm(WaterForm):
    action = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='country_form')
    people_number = forms.IntegerField(min_value=0)

