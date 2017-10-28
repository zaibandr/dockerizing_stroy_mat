from django.forms import Select


class MySelect(Select):
    def render_option(self, selected_choices, option_value, option_label):
        # look at the original for something to start with
        return '<option value="{}" data-tokens="{}">{}</option>'.format(option_value, str(option_label).lower(), option_label)