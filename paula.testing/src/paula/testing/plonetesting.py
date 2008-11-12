from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup, PloneSite
from Products.PloneTestCase.PloneTestCase import setupPloneSite

from plone.app.controlpanel.tests import ControlPanelTestCase
from kss.core.tests.base import KSSLayer, KSSViewTestCase

from paula.testing.testing import my_import

@onsetup
def setup_package(pkg_name):
    """
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    
    # Load the ZCML configuration for the optilux.policy package.
    # This includes the other products below as well.
    
    fiveconfigure.debug_mode = True

    mod = my_import(pkg_name)
    zcml.load_config('ftesting.zcml', mod)
    fiveconfigure.debug_mode = False
    
    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML.
    
    ztc.installPackage(pkg_name)
    
class PloneTestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """
        
class FunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """

class PanelTestCase(FunctionalTestCase, ControlPanelTestCase):
    """Test case used for the control panel tests, with some convenience 
    methods from plone.app.controlpanel.
    """
    
class KSSTestCase(FunctionalTestCase, KSSViewTestCase):
    """Test case used for KSS tests
    """
    
    class layer(KSSLayer, PloneSite):
        pass
