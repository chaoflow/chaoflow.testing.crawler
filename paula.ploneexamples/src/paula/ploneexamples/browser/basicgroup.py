from zope.component import createObject
from zope.formlib import form

from plone.app.form import base

from paula.examples.interfaces import IBasicGroup


basicgroup_form_fields = form.Fields(IBasicGroup)
        
class BasicGroupAddForm(base.AddForm):
    """Add form for Basic Groups
    """
    
    form_fields = basicgroup_form_fields
    
    label = u"Add Basic Group"
    form_name = u"Basic Group settings"
    
    def create(self, data):
        basicgroup = createObject(u"paula.ploneexamples.BasicGroup")
        form.applyChanges(basicgroup, self.form_fields, data)
        return basicgroup
    

class BasicGroupEditForm(base.EditForm):
    """Edit form for Basic Groups
    """
    
    form_fields = basicgroup_form_fields
    
    label = u"Edit Basic Group"
    form_name = u"Basic Group settings"
