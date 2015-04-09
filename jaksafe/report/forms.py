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

class AggregateForm(forms.Form):
    aggregate_file = forms.FileField(
        label="",
        help_text="Must be a CSV file.",
    )
    
    def clean_aggregate_file(self):
        aggregate_file = self.cleaned_data['aggregate_file']
        content_type = aggregate_file.content_type.split('/')[1]
        size = aggregate_file._size
        
        print 'DEBUG %s' % content_type
        
        if content_type in settings.CONTENT_TYPES:
            if size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_("File size is over %s. Current file size %s.") % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(size)))
        else:
            raise forms.ValidationError(_('File type is not supported.'))
        
        return aggregate_file

class AssumptionsDamageForm(forms.Form):
    assumptions_damage_file = forms.FileField(
        label="",
        help_text="Must be a CSV file.",
    )
    
    def clean_assumptions_damage_file(self):
        the_file = self.cleaned_data['assumptions_damage_file']
        content_type = the_file.content_type.split('/')[1]
        size = the_file._size
        
        print 'DEBUG %s' % content_type
        
        if content_type in settings.CONTENT_TYPES:
            if size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_("File size is over %s. Current file size %s.") % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(size)))
        else:
            raise forms.ValidationError(_('File type is not supported.'))
        
        return the_file

class AssumptionsLossForm(forms.Form):
    assumptions_loss_file = forms.FileField(
        label="",
        help_text="Must be a CSV file.",
    )
    
    def clean_assumptions_loss_file(self):
        the_file = self.cleaned_data['assumptions_loss_file']
        content_type = the_file.content_type.split('/')[1]
        size = the_file._size
        
        print 'DEBUG %s' % content_type
        
        if content_type in settings.CONTENT_TYPES:
            if size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_("File size is over %s. Current file size %s.") % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(size)))
        else:
            raise forms.ValidationError(_('File type is not supported.'))
        
        return the_file

class AssumptionsAggregateForm(forms.Form):
    assumptions_aggregate_file = forms.FileField(
        label="",
        help_text="Must be a CSV file.",
    )
    
    def clean_assumptions_aggregate_file(self):
        the_file = self.cleaned_data['assumptions_aggregate_file']
        content_type = the_file.content_type.split('/')[1]
        size = the_file._size
        
        print 'DEBUG %s' % content_type
        
        if content_type in settings.CONTENT_TYPES:
            if size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_("File size is over %s. Current file size %s.") % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(size)))
        else:
            raise forms.ValidationError(_('File type is not supported.'))
        
        return the_file

class AssumptionsInsuranceForm(forms.Form):
    assumptions_insurance_file = forms.FileField(
        label="",
        help_text="Must be a CSV file.",
    )
    
    def clean_assumptions_insurance_file(self):
        the_file = self.cleaned_data['assumptions_insurance_file']
        content_type = the_file.content_type.split('/')[1]
        size = the_file._size
        
        print 'DEBUG %s' % content_type
        
        if content_type in settings.CONTENT_TYPES:
            if size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_("File size is over %s. Current file size %s.") % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(size)))
        else:
            raise forms.ValidationError(_('File type is not supported.'))
        
        return the_file

class AssumptionsInsurancePenetrationForm(forms.Form):
    assumptions_insurance_penetration_file = forms.FileField(
        label="",
        help_text="Must be a CSV file.",
    )
    
    def clean_assumptions_insurance_penetration_file(self):
        the_file = self.cleaned_data['assumptions_insurance_penetration_file']
        content_type = the_file.content_type.split('/')[1]
        size = the_file._size
        
        print 'DEBUG %s' % content_type
        
        if content_type in settings.CONTENT_TYPES:
            if size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_("File size is over %s. Current file size %s.") % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(size)))
        else:
            raise forms.ValidationError(_('File type is not supported.'))
        
        return the_file