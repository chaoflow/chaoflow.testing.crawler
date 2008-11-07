from zope.component import createObject
from zope.formlib import form

from plone.app.form import base

from paula.examples.interfaces import IMinimalPloneUser


minplone_form_fields = form.Fields(IMinimalPloneUser)
        
class MinimalPloneUserAddForm(base.AddForm):
    """Add form for Minimal Plone Users
    """
    
    form_fields = minplone_form_fields
    
    label = u"Add Minimal Plone User"
    form_name = u"Minimal Plone User settings"
    
    def create(self, data):
        minplone = createObject(u"paula.ploneexamples.MinimalPloneUser")
        form.applyChanges(minplone, self.form_fields, data)
        return minplone
    

class MinimalPloneUserEditForm(base.EditForm):
    """Edit form for Minimal Plone Users
    """
    
    form_fields = minplone_form_fields
    
    label = u"Edit Minimal Plone User"
    form_name = u"Minimal Plone User settings"
