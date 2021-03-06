from django import forms
from .models import Question, Profile, Profile_Choice_Selection, Service
from django.forms.widgets import RadioFieldRenderer, Select
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.forms.widgets import CheckboxFieldRenderer, Select
import numpy as np


class ProfileDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileDataForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'profileform'})
            if field.label == "Einverständnis":
                field.required = True
    class Meta:
        model = Profile
        exclude = ['date_posted', 'selected_service', 'empty_profile', 'remarks', 'deleted', 'assigned', 'status']
        

class NewProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
                field.widget.attrs.update({'class' : 'profileform'})
    class Meta:
        model = Profile
        exclude = ['empty_profile', 'deleted']


class ProfileDataEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileDataEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
                field.widget.attrs.update({'class' : 'profileform'})
    class Meta:
        model = Profile
        exclude = ['empty_profile', 'deleted', 'accepted_terms']


class SkipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SkipForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
                field.widget.attrs.update({'class' : 'profileform'})
                if field.label == "Einverständnis":
                    field.required = True
    class Meta:
        model = Profile
        exclude = ['date_posted', 'phone_number', 'occupation', 'street', 'city',
                   'message', 'selected_service', 'empty_profile', 'remarks', 'deleted', 'assigned']


class BaseChoiceForm(forms.Form):
    def pk_bool_array(self):
        raise NotImplementedError("Please Implement this method")

    def save(self, profile):
        profile_choice_objects = self.create_objects(profile)
        # save all to db
        Profile_Choice_Selection.objects.bulk_create(profile_choice_objects)

    def create_objects(self, profile):
        assert (self.is_valid())
        profile_choice_objects = []
        for choice, selected in self.pk_bool_array():
            profile_choice_objects.append(Profile_Choice_Selection(profile=profile, choice=choice, selected=selected))
        return profile_choice_objects

class InterestsForm(BaseChoiceForm):
    def __init__(self, *args, **kwargs):
        super(InterestsForm, self).__init__(*args, **kwargs)
        self.question = Question.objects.get(question_identifier="interests")
        self.choice_dict = self.question.get_choices_as_dict()

        self.criteria_pk_dict = {}
        for criteria, criteria_choices in self.choice_dict.items():
            self.criteria_pk_dict[criteria] = [pk for pk, c in criteria_choices]

        self.question_text = self.question.question_text
        self.choice_options = ["Sehr Interessiert", "Interessiert", "Weniger Interessiert"]
        assert set(self.choice_options) == set(self.question.get_choice_options())

        for criteria, criteria_choices in self.choice_dict.items():
            choices = [(pk, c) for pk, c in criteria_choices]
            self.fields[criteria] = forms.ChoiceField(label=criteria, widget=RowSelectWidget, choices=choices)

    def is_valid(self):
        return all([int(self.data[criteria]) in pks for criteria, pks in self.criteria_pk_dict.items()])

    def pk_bool_array(self):
        assert (self.is_valid())
        selected_pks = [int(self.data[criteria]) for criteria in self.choice_dict]
        pk_bool_array = [(c, c.pk in selected_pks) for c in self.question.get_choices()]
        assert np.sum([int(selected) for _, selected in pk_bool_array]) == len(self.choice_dict)
        assert len(pk_bool_array) == len(self.question.get_choices())
        return pk_bool_array

class SkillsForm1(BaseChoiceForm):
    def __init__(self, *args, num_selectors=1, num_required_fields=1, **kwargs):
        super(SkillsForm1, self).__init__(*args, **kwargs)

        self.question = Question.objects.get(question_identifier="skills1")
        choices = [(c.pk, c.choice_text) for c in self.question.get_choices()]
        self.fields["skills1"] = forms.ChoiceField(label="", choices=choices, widget=RowChoiceWidget2)

    def is_valid(self):
        try:
            return int(self.data["skills1"]) in [c.pk for c in self.question.get_choices()]
        except:
            return False

    def pk_bool_array(self):
        assert (self.is_valid())
        selected_pk = int(self.data["skills1"])
        return [(c, c.pk == selected_pk) for c in self.question.get_choices()]

class SkillsForm2(BaseChoiceForm):
    def __init__(self, *args, **kwargs):
        super(SkillsForm2, self).__init__(*args, **kwargs)

        self.question = Question.objects.get(question_identifier="skills2")
        choices = [(c.pk, c.choice_text) for c in self.question.get_choices()]
        self.fields["skills2"] = forms.ChoiceField(label="", choices=choices, widget=RowChoiceWidget)

    def is_valid(self):
        try:
            return int(self.data["skills2"]) in [c.pk for c in self.question.get_choices()]
        except:
            return False

    def pk_bool_array(self):
        assert (self.is_valid())
        selected_pk = int(self.data["skills2"])
        return [(c, c.pk == selected_pk) for c in self.question.get_choices()]

class SkillsForm3(BaseChoiceForm):
    def __init__(self, *args, **kwargs):
        super(SkillsForm3, self).__init__(*args, **kwargs)
        self.question = Question.objects.get(question_identifier="skills3")

        #age = forms.IntegerField()
        self.fields["skills3"] = forms.IntegerField(label="")

        choices = [(c.pk, c.choice_text) for c in self.question.get_choices()]
        self.fields["skills3"] = forms.ChoiceField(label="", choices=choices, widget=RowChoiceWidget)

    def is_valid(self):
        try:
            return int(self.data["skills3"]) in [c.pk for c in self.question.get_choices()]
        except:
            return False

    def pk_bool_array(self):
        assert (self.is_valid())
        selected_pk = int(self.data["skills3"])
        return [(c, c.pk == selected_pk) for c in self.question.get_choices()]


#
# Customized Renderers / Widgets
#

class RowWidgetRenderer(RadioFieldRenderer):
    outer_html = '{content}'
    inner_html = '<div class="col-xs-2" style="text-align: center"> <div class="checkbox"> {choice_value}{sub_widgets}</div> </div>'

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

class RowWidgetRendererCheckbox(CheckboxFieldRenderer):
    outer_html = '{content}'
    inner_html = '<div class="col-xs-6" style=""> <div class="checkbox skills"> {choice_value}{sub_widgets}</div> </div>'

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

class RowChoiceWidget2(forms.CheckboxSelectMultiple):
    renderer = RowWidgetRendererCheckbox


def safe_all_forms(session, empty_profile=False, skip_profile=False):
    assert 'skills_post' in session
    assert 'interests_post' in session

    if empty_profile:#user wants to skip the profile form --> create empty profile object with empty flag set
        profile = Profile.create_empty_profile()
    elif skip_profile:#user did not fill in all profile data
        assert 'profile_post' in session
        profile = SkipForm(session['profile_post']).save()

    else:
        assert 'profile_post' in session
        profile = ProfileDataForm(session['profile_post']).save()

    if 'results_post' in session:
        profile.selected_service = Service.objects.get(pk=int(session['results_post']['service']))
    profile.save()

    SkillsForm1(session['skills_post']).save(profile)
    SkillsForm2(session['skills_post']).save(profile)
    SkillsForm3(session['skills_post']).save(profile)
    InterestsForm(session['interests_post']).save(profile)


def choice_array(session):
    assert 'skills_post' in session
    assert 'interests_post' in session
    choice_array = []
    choice_array.extend(SkillsForm1(session['skills_post']).pk_bool_array())
    choice_array.extend(SkillsForm2(session['skills_post']).pk_bool_array())
    choice_array.extend( InterestsForm(session['interests_post']).pk_bool_array())
    return choice_array
