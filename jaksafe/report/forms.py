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

class BoundaryForm(forms.Form):
    boundary_shp_file = forms.FileField(
        label="",
        help_text="Must be a SHP file",
    )
    
    boundary_shx_file = forms.FileField(
        label="",
        help_text="Must be a SHX file",
    )
    
    boundary_dbf_file = forms.FileField(
        label="",
        help_text="Must be a DBF file",
    )
    
    boundary_prj_file = forms.FileField(
        label="",
        help_text="Must be a PRJ file",
    )
    
    boundary_qpj_file = forms.FileField(
        label="",
        help_text="Must be a QPJ file",
    )
    
    def clean(self):
        boundary_shp_file = self.cleaned_data.get('boundary_shp_file')
        boundary_shx_file = self.cleaned_data.get('boundary_shx_file')
        boundary_dbf_file = self.cleaned_data.get('boundary_dbf_file')
        boundary_prj_file = self.cleaned_data.get('boundary_prj_file')
        boundary_qpj_file = self.cleaned_data.get('boundary_qpj_file')
        
        if (boundary_shp_file == False or boundary_shx_file == False or boundary_dbf_file == False or boundary_prj_file == False or boundary_qpj_file == False):
            raise forms.ValidationError(_('Upload file not found.'))
        
        if boundary_shp_file:
            filename = boundary_shp_file.name
            content_type = boundary_shp_file.content_type.split('/')[1]
            size = boundary_shp_file._size
            
            if (filename.lower().endswith('.shp') == False):
                print 'DEBUG invalid file type'
                raise forms.ValidationError(_('Invalid file type.'))
            
            print 'DEBUG %s %s %s' % (filename, content_type, size)
        
        if boundary_shx_file:
            filename = boundary_shx_file.name
            content_type = boundary_shx_file.content_type.split('/')[1]
            size = boundary_shx_file._size
            
            if (filename.lower().endswith('.shx') == False):
                print 'DEBUG invalid file type'
                raise forms.ValidationError(_('Invalid file type.'))
            
            print 'DEBUG %s %s %s' % (filename, content_type, size)
        
        if boundary_dbf_file:
            filename = boundary_dbf_file.name
            content_type = boundary_dbf_file.content_type.split('/')[1]
            size = boundary_dbf_file._size
            
            if (filename.lower().endswith('.dbf') == False):
                print 'DEBUG invalid file type'
                raise forms.ValidationError(_('Invalid file type.'))
            
            print 'DEBUG %s %s %s' % (filename, content_type, size)
        
        if boundary_prj_file:
            filename = boundary_prj_file.name
            content_type = boundary_prj_file.content_type.split('/')[1]
            size = boundary_prj_file._size
            
            if (filename.lower().endswith('.prj') == False):
                print 'DEBUG invalid file type'
                raise forms.ValidationError(_('Invalid file type.'))
            
            print 'DEBUG %s %s %s' % (filename, content_type, size)
        
        if boundary_qpj_file:
            filename = boundary_qpj_file.name
            content_type = boundary_qpj_file.content_type.split('/')[1]
            size = boundary_qpj_file._size
            
            if (filename.lower().endswith('.qpj') == False):
                print 'DEBUG invalid file type'
                raise forms.ValidationError(_('Invalid file type.'))
            
            print 'DEBUG %s %s %s' % (filename, content_type, size)

class BuildingExposureForm(forms.Form):
    building_exposure_shp_file = forms.FileField(
        label="",
        help_text="Must be a SHP file",
    )
    
    building_exposure_shx_file = forms.FileField(
        label="",
        help_text="Must be a SHX file",
    )
    
    building_exposure_dbf_file = forms.FileField(
        label="",
        help_text="Must be a DBF file",
    )
    
    building_exposure_prj_file = forms.FileField(
        label="",
        help_text="Must be a PRJ file",
    )
    
    building_exposure_qpj_file = forms.FileField(
        label="",
        help_text="Must be a QPJ file",
    )
    
    def clean(self):
        building_exposure_shp_file = self.cleaned_data.get('building_exposure_shp_file')
        building_exposure_shx_file = self.cleaned_data.get('building_exposure_shx_file')
        building_exposure_dbf_file = self.cleaned_data.get('building_exposure_dbf_file')
        building_exposure_prj_file = self.cleaned_data.get('building_exposure_prj_file')
        building_exposure_qpj_file = self.cleaned_data.get('building_exposure_qpj_file')
        
        if (building_exposure_shp_file == False or building_exposure_shx_file == False or building_exposure_dbf_file == False or building_exposure_prj_file == False or building_exposure_qpj_file == False):
            raise forms.ValidationError(_('Upload file not found.'))
        
        if building_exposure_shp_file:
            filename = building_exposure_shp_file.name
            content_type = building_exposure_shp_file.content_type.split('/')[1]
            size = building_exposure_shp_file._size
            
            if (filename.lower().endswith('.shp') == False):
                print 'DEBUG invalid file type'
                raise forms.ValidationError(_('Invalid file type.'))
            
            print 'DEBUG %s %s %s' % (filename, content_type, size)
        
        if building_exposure_shx_file:
            filename = building_exposure_shx_file.name
            content_type = building_exposure_shx_file.content_type.split('/')[1]
            size = building_exposure_shx_file._size
            
            if (filename.lower().endswith('.shx') == False):
                print 'DEBUG invalid file type'
                raise forms.ValidationError(_('Invalid file type.'))
            
            print 'DEBUG %s %s %s' % (filename, content_type, size)
        
        if building_exposure_dbf_file:
            filename = building_exposure_dbf_file.name
            content_type = building_exposure_dbf_file.content_type.split('/')[1]
            size = building_exposure_dbf_file._size
            
            if (filename.lower().endswith('.dbf') == False):
                print 'DEBUG invalid file type'
                raise forms.ValidationError(_('Invalid file type.'))
            
            print 'DEBUG %s %s %s' % (filename, content_type, size)
        
        if building_exposure_prj_file:
            filename = building_exposure_prj_file.name
            content_type = building_exposure_prj_file.content_type.split('/')[1]
            size = building_exposure_prj_file._size
            
            if (filename.lower().endswith('.prj') == False):
                print 'DEBUG invalid file type'
                raise forms.ValidationError(_('Invalid file type.'))
            
            print 'DEBUG %s %s %s' % (filename, content_type, size)
        
        if building_exposure_qpj_file:
            filename = building_exposure_qpj_file.name
            content_type = building_exposure_qpj_file.content_type.split('/')[1]
            size = building_exposure_qpj_file._size
            
            if (filename.lower().endswith('.qpj') == False):
                print 'DEBUG invalid file type'
                raise forms.ValidationError(_('Invalid file type.'))
            
            print 'DEBUG %s %s %s' % (filename, content_type, size)

class RoadExposureForm(forms.Form):
    road_exposure_shp_file = forms.FileField(
        label="",
        help_text="Must be a SHP file",
    )
    
    road_exposure_shx_file = forms.FileField(
        label="",
        help_text="Must be a SHX file",
    )
    
    road_exposure_dbf_file = forms.FileField(
        label="",
        help_text="Must be a DBF file",
    )
    
    road_exposure_prj_file = forms.FileField(
        label="",
        help_text="Must be a PRJ file",
    )
    
    road_exposure_qpj_file = forms.FileField(
        label="",
        help_text="Must be a QPJ file",
    )
    
    def clean(self):
        road_exposure_shp_file = self.cleaned_data.get('road_exposure_shp_file')
        road_exposure_shx_file = self.cleaned_data.get('road_exposure_shx_file')
        road_exposure_dbf_file = self.cleaned_data.get('road_exposure_dbf_file')
        road_exposure_prj_file = self.cleaned_data.get('road_exposure_prj_file')
        road_exposure_qpj_file = self.cleaned_data.get('road_exposure_qpj_file')
        
        if (road_exposure_shp_file == False or road_exposure_shx_file == False or road_exposure_dbf_file == False or road_exposure_prj_file == False or road_exposure_qpj_file == False):
            raise forms.ValidationError(_('Upload file not found.'))
        
        if road_exposure_shp_file:
            filename = road_exposure_shp_file.name
            content_type = road_exposure_shp_file.content_type.split('/')[1]
            size = road_exposure_shp_file._size
            
            if (filename.lower().endswith('.shp') == False):
                print 'DEBUG invalid file type'
                raise forms.ValidationError(_('Invalid file type.'))
            
            print 'DEBUG %s %s %s' % (filename, content_type, size)
        
        if road_exposure_shx_file:
            filename = road_exposure_shx_file.name
            content_type = road_exposure_shx_file.content_type.split('/')[1]
            size = road_exposure_shx_file._size
            
            if (filename.lower().endswith('.shx') == False):
                print 'DEBUG invalid file type'
                raise forms.ValidationError(_('Invalid file type.'))
            
            print 'DEBUG %s %s %s' % (filename, content_type, size)
        
        if road_exposure_dbf_file:
            filename = road_exposure_dbf_file.name
            content_type = road_exposure_dbf_file.content_type.split('/')[1]
            size = road_exposure_dbf_file._size
            
            if (filename.lower().endswith('.dbf') == False):
                print 'DEBUG invalid file type'
                raise forms.ValidationError(_('Invalid file type.'))
            
            print 'DEBUG %s %s %s' % (filename, content_type, size)
        
        if road_exposure_prj_file:
            filename = road_exposure_prj_file.name
            content_type = road_exposure_prj_file.content_type.split('/')[1]
            size = road_exposure_prj_file._size
            
            if (filename.lower().endswith('.prj') == False):
                print 'DEBUG invalid file type'
                raise forms.ValidationError(_('Invalid file type.'))
            
            print 'DEBUG %s %s %s' % (filename, content_type, size)
        
        if road_exposure_qpj_file:
            filename = road_exposure_qpj_file.name
            content_type = road_exposure_qpj_file.content_type.split('/')[1]
            size = road_exposure_qpj_file._size
            
            if (filename.lower().endswith('.qpj') == False):
                print 'DEBUG invalid file type'
                raise forms.ValidationError(_('Invalid file type.'))
            
            print 'DEBUG %s %s %s' % (filename, content_type, size)