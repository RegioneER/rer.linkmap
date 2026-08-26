from AccessControl import Unauthorized
from Acquisition import aq_base
from json import dumps
from lxml import etree
from plone import api
from plone.registry.interfaces import IRegistry
from Products.Five import BrowserView
from rer.linkmap.linkmap import CATEGORY_C1
from rer.linkmap.linkmap import CATEGORY_KEYS
from rer.linkmap.linkmap import ensure_required_root_url
from rer.linkmap.linkmap import is_valid_date
from rer.linkmap.linkmap import is_valid_url
from rer.linkmap.linkmap import today_date_string
from urllib.parse import urlsplit
from urllib.parse import urlunsplit
from zExceptions import NotFound
from zope.component import getUtility

try:
    from plone.volto.interfaces import IVoltoSettings

    HAS_PLONE_VOLTO = True
except ImportError:
    HAS_PLONE_VOLTO = False

REGISTRY_PREFIX = "rer.linkmap.controlpanels.settings.ILinkMapSettings"
ROOT_KEY = "amministrazione_trasparente"
NAMESPACE = "https://guida-servizi.anticorruzione.it/trasparenza"


def get_registry_value(field_name, default=""):
    return api.portal.get_registry_record(
        f"{REGISTRY_PREFIX}.{field_name}",
        default=default,
    )


def get_expose_json():
    return get_registry_value("expose_json", default=False)


def get_expose_xml():
    return get_registry_value("expose_xml", default=False)


def get_data_ultima_modifica():
    value = get_registry_value("data_ultima_modifica")
    if is_valid_date(value):
        return value
    return today_date_string()


def get_frontend_url():
    """Return the public (frontend) base url for this Plone site.

    Editors fill in the category fields as plain absolute urls, and they
    often copy them while browsing the backend, so internal links may end
    up with the backend/IAM domain baked in. Falls back to the current
    portal absolute_url() when plone.volto is not installed or
    ``volto.frontend_domain`` has not been configured.
    """
    portal_url = api.portal.get().absolute_url()
    if not HAS_PLONE_VOLTO:
        return portal_url
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IVoltoSettings, prefix="volto", check=False)
    frontend_domain = (getattr(settings, "frontend_domain", "") or "").rstrip("/")
    if not frontend_domain or frontend_domain == "http://localhost:3000":
        return portal_url
    return frontend_domain


def resolve_internal_url(value, frontend_url):
    """If ``value`` points to an object inside this Plone site, rewrite it
    so that it always uses the public frontend domain, regardless of the
    domain that was used to author it (e.g. the backend/IAM domain).
    External urls are returned unchanged.
    """
    parsed = urlsplit(value)
    path = parsed.path.strip("/")
    if not path:
        return value
    portal = api.portal.get()
    try:
        target = portal.unrestrictedTraverse(path, None)
    except (AttributeError, KeyError, TypeError, ValueError, Unauthorized):
        target = None
    if target is None:
        return value
    frontend_parts = urlsplit(frontend_url)
    return urlunsplit(
        (
            frontend_parts.scheme,
            frontend_parts.netloc,
            parsed.path,
            parsed.query,
            parsed.fragment,
        )
    )


def build_category_map_from_fields(frontend_url):
    """Build category map from individual field values."""
    category_map = {}
    for key in CATEGORY_KEYS:
        value = get_registry_value(key)
        if value and is_valid_url(value.strip()):
            category_map[key] = resolve_internal_url(value.strip(), frontend_url)
    return category_map


def build_payload():
    data_ultima_modifica = get_data_ultima_modifica()
    frontend_url = get_frontend_url()
    category_map = build_category_map_from_fields(frontend_url)
    ensure_required_root_url(category_map, frontend_url)

    payload = {
        "data_ultima_modifica": data_ultima_modifica,
        CATEGORY_C1: category_map,
    }
    return payload


def _qname(tag):
    return f"{{{NAMESPACE}}}{tag}"


def _serialize_xml(root):
    return etree.tostring(
        root, xml_declaration=True, encoding="utf-8", pretty_print=True
    ).decode("utf-8")


def build_xml(payload):
    root = etree.Element(_qname("amministrazione_trasparente"), nsmap={None: NAMESPACE})

    data_node = etree.SubElement(root, _qname("data_ultima_modifica"))
    data_node.text = payload["data_ultima_modifica"]

    map_node = etree.SubElement(root, _qname("map"))

    category = CATEGORY_C1
    category_node = etree.SubElement(map_node, _qname(category))
    map_values = payload.get(category, {})
    for map_key in CATEGORY_KEYS:
        map_url = map_values.get(map_key)
        if not map_url:
            continue
        key_node = etree.SubElement(category_node, _qname(map_key))
        key_node.text = map_url

    return _serialize_xml(root)


class ATMapJSONView(BrowserView):
    def __call__(self):
        if aq_base(self.context) is not aq_base(api.portal.get()):
            raise NotFound()
        if not get_expose_json():
            raise NotFound()
        self.request.response.setHeader(
            "Content-Type", "application/json; charset=utf-8"
        )
        payload = build_payload()
        return dumps(payload, indent=2, ensure_ascii=False)


class ATMapXMLView(BrowserView):
    def __call__(self):
        if aq_base(self.context) is not aq_base(api.portal.get()):
            raise NotFound()
        if not get_expose_xml():
            raise NotFound()
        self.request.response.setHeader(
            "Content-Type", "application/xml; charset=utf-8"
        )
        payload = build_payload()
        return build_xml(payload)
