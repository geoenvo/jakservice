from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.conf import settings

class ImpactClassForm(forms.Form):
    impact_class_file = forms.FileField(
        label="",
        help_text="Must be a CSV file.",
    )
    
    def clean_impact_class_file(self):
        impact_class_file = self.cleaned_data['impact_class_file']
        content_type = impact_class_file.content_type.split('/')[1]
        size = impact_class_file._size
        
        print 'DEBUG %s' % content_type
        
        if content_type in settings.CONTENT_TYPES:
            if size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_("File size is over %s. Current file size %s.") % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(size)))
        else:
            raise forms.ValidationError(_('File type is not supported.'))
        
        return impact_class_file