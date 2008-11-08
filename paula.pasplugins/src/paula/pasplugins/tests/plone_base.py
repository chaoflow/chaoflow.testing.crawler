from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup, PloneSite

from plone.app.controlpanel.tests import ControlPanelTestCase
from kss.core.tests.base import KSSLayer, KSSViewTestCase

@onsetup
def setup_paula_pasplugins():
    """Set up the additional products required for the Optilux Cinema Content.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    
    # Load the ZCML configuration for the optilux.policy package.
    # This includes the other products below as well.
    
    fiveconfigure.debug_mode = True
    import paula.pasplugins
    zcml.load_config('ftesting.zcml', paula.pasplugins)
    fiveconfigure.debug_mode = False
    
    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML.
    
    ztc.installPackage('paula.pasplugins')
    
# The order here is important: We first call the (deferred) function which
# installs the products we need for the Optilux package. Then, we let 
# PloneTestCase set up this product on installation.

setup_paula_pasplugins()
ptc.setupPloneSite(products=['paula.pasplugins'])

class PaulaTestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """
        
class PaulaFunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """

class PaulaPanelTestCase(PaulaFunctionalTestCase, ControlPanelTestCase):
    """Test case used for the control panel tests, with some convenience 
    methods from plone.app.controlpanel.
    """
    
class PaulaKSSTestCase(PaulaFunctionalTestCase, KSSViewTestCase):
    """Test case used for KSS tests
    """
    
    class layer(KSSLayer, PloneSite):
        pass
