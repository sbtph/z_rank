from django.forms import Form as F
from django.forms.fields import IntegerField as I

class AddForm(F):
    a = I()
    b = I()