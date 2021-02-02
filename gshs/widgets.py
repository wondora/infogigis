from django import forms

class AutoCompleteWidget(forms.Select):
    template_name = 'gshs/widgets/autocomplete_select.html'

    class Media:
        css = {
            'all' : [
                "//cdnjs.cloudflare.com/ajax/libs/select2/4.0.8/css/select2.min.css",
            ],
        }
        js = [   
            "//code.jquery.com/jquery-3.4.1.min.js",   
            "//cdnjs.cloudflare.com/ajax/libs/select2/4.0.8/js/select2.min.js",
        ]

    def build_attrs(self, *args, **kwargs):
        context = super().build_attrs(*args, **kwargs)
        context['style'] = 'min-width:200px;'
        return context

    def __init__(self, ajax_url, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ajax_url = ajax_url

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context['ajax_url'] = self.ajax_url
        return context

    def optgroups(self, name, value, attrs=None):
        existed_ids = [_id for _id in value if _id]
        self.choices.queryset = self.choices.queryset.filter(id__in=existed_ids)
        return super().optgroups(name, value, attrs=None)

class DatePickerWidget(forms.DateInput):
    template_name = "gshs/widgets/picker_date.html"

    class Media:
        css = {
            'all': [
                "//cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/themes/base/jquery-ui.min.css",
            ],
        }

        js = [    
            "//code.jquery.com/jquery-3.4.1.min.js",
            "//cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
        ]
