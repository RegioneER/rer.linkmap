from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.restapi.controlpanels.interfaces import IControlpanel
from redturtle.linkmap.controlpanels.settings import ILinkMapSettings
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class ILinkMapSettingsControlpanel(IControlpanel):
    """Marker interface for LinkMap settings control panel"""


@adapter(Interface, Interface)
@implementer(ILinkMapSettingsControlpanel)
class LinkMapSettings(RegistryConfigletPanel):
    schema = ILinkMapSettings
    configlet_id = "RedturtleLinkMapSettings"
    configlet_category_id = "Products"
    schema_prefix = None
