from django import forms
from .models import Question, Profile
from django.forms.widgets import RadioFieldRenderer
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text

"""
class ProfileDataForm(forms.Form):
    first_name = forms.CharField(label='Vorname ', max_length=30)
    last_name = forms.CharField(label='Nachname ', max_length=50)
    email = forms.EmailField(label='E-Mail')
    phone_number = forms.CharField(label='Telefonnummer', max_length=20, required=False)
    occupation = forms.CharField(label='Beruf', max_length=40)
    street = forms.CharField(label='Adresse', max_length=40)
    zip_code = forms.CharField(label='PLZ', max_length=10)
    city =  forms.CharField(label='Wohnort', max_length=40)
    message = forms.CharField(widget=forms.Textarea, label='Nachricht', max_length=1000, required=False)
"""

class ProfileDataForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['date_posted']


class InterestsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(InterestsForm, self).__init__(*args, **kwargs)
        question = Question.objects.get(question_identifier="interests")
        coice_dict = question.get_choices_as_dict()

        self.question_text = question.question_text
        self.choice_options = ["Interessiert", "Aufgeschlossen", "Nicht Interessiert"]
        assert set(self.choice_options) == set(question.get_choice_options())

        for criteria, criteria_choices in coice_dict.items():
            choices = [(str(i),c) for i, c in enumerate(criteria_choices)]
            self.fields[criteria] = forms.ChoiceField(label=criteria, widget=RowSelectWidget, choices=choices)


class RowWidgetRenderer(RadioFieldRenderer):
    outer_html = '{content}'
    inner_html = '<div class="col-xs-2"> <div class="checkbox"> {choice_value}{sub_widgets}</div> </div>'

    def render(self):
        """
        Outputs a <ul> for this set of choice fields.
        If an id was given to the field, it is applied to the <ul> (each
        item in the list will get an id of `$id_$i`).
        """
        id_ = self.attrs.get('id')
        output = []
        for i, choice in enumerate(self.choices):
            choice_value, choice_label = choice
            if isinstance(choice_label, (tuple, list)):
                attrs_plus = self.attrs.copy()
                if id_:
                    attrs_plus['id'] += '_{}'.format(i)
                sub_ul_renderer = self.__class__(
                    name=self.name,
                    value=self.value,
                    attrs=attrs_plus,
                    choices=choice_label,
                )
                sub_ul_renderer.choice_input_class = self.choice_input_class
                output.append(format_html(
                    self.inner_html, choice_value=choice_value,
                    sub_widgets=sub_ul_renderer.render(),
                ))
            else:
                w = self.choice_input_class(self.name, self.value, self.attrs.copy(), choice, i)
                w.choice_label=""
                output.append(format_html(self.inner_html, choice_value=force_text(w), sub_widgets=''))
        return format_html(
            self.outer_html,
            id_attr=format_html(' id="{}"', id_) if id_ else '',
            content=mark_safe('\n'.join(output)),
        )

class RowSelectWidget(forms.RadioSelect):
    renderer = RowWidgetRenderer

