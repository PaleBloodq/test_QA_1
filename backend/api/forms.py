from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from settings import settings


class DragAndDropFileInput(forms.ClearableFileInput):
    template_name = 'admin/drag_and_drop_file_input.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['BASE_URL'] = settings.FORCE_SCRIPT_NAME
        return context


class ManyToManyForm(FilteredSelectMultiple):
    def __init__(self) -> None:
        super().__init__(' ', False)
