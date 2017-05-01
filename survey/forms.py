from django import forms
from .models import Question, Profile
from django.forms.widgets import RadioFieldRenderer, Select
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text


class ProfileDataForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['date_posted']

class InterestsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(InterestsForm, self).__init__(*args, **kwargs)
        question = Question.objects.get(question_identifier="interests")
        self.coice_dict = question.get_choices_as_dict()

        self.question_text = question.question_text
        self.choice_options = ["Interessiert", "Aufgeschlossen", "Nicht Interessiert"]
        assert set(self.choice_options) == set(question.get_choice_options())

        for criteria, criteria_choices in self.coice_dict.items():
            choices = [(c,c) for c in criteria_choices]
            self.fields[criteria] = forms.ChoiceField(label=criteria, widget=RowSelectWidget, choices=choices)

    def is_valid(self):
        return all([self.data[criteria] in criteria_choices for criteria, criteria_choices in self.coice_dict.items()])

class SkillsForm1(forms.Form):
    def __init__(self, *args, num_selectors=1, num_required_fields=1, **kwargs):
        super(SkillsForm1, self).__init__(*args, **kwargs)

        self.num_required_fields = num_required_fields
        self.question = Question.objects.get(question_identifier="skills1")
        choices = [('', '')] + [(c.choice_text, c.choice_text) for c in self.question.get_choices()]

        for i in range(num_selectors):
            required = i < num_required_fields
            self.fields['skills1_' + str(i)] = forms.ChoiceField(widget=Select(attrs={'class': "form-control"}), choices=choices, label='', required=required)

    def is_valid(self):
        selected_skills = [self.data[field_name] for field_name in self.fields.keys() if self.data[field_name] != '']
        valid_skill_choices = [c.choice_text for c in self.question.get_choices()]
        valid_values = all([skill in valid_skill_choices for skill in selected_skills])
        enough_skills_selected = len(set(selected_skills)) >= self.num_required_fields
        return valid_values and enough_skills_selected

class SkillsForm2(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SkillsForm2, self).__init__(*args, **kwargs)

        self.question = Question.objects.get(question_identifier="skills2")
        choices = [(c.choice_text, c.choice_text) for c in self.question.get_choices()]
        self.fields["skills2"] = forms.ChoiceField(label="", choices=choices, widget=RowChoiceWidget)

    def is_valid(self):
        return self.data["skills2"] in [c.choice_text for c in self.question.get_choices()]

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

class RowChoiceRenderer(RadioFieldRenderer):
    def __init__(self, *args, **kwargs):
        super(RowChoiceRenderer, self).__init__(*args, **kwargs)
        self.outer_html = '{content}'
        self.inner_html = '<div class="checkbox"> {choice_value}{sub_widgets}</div>'

class RowChoiceWidget(forms.RadioSelect):
    renderer = RowChoiceRenderer



