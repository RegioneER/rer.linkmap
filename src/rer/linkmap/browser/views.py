from Acquisition import aq_base
from json import dumps
from plone import api
from plone.registry.interfaces import IRegistry
from plone.volto.interfaces import IVoltoSettings
from Products.Five import BrowserView
from rer.linkmap.linkmap import CATEGORY_C1
from rer.linkmap.linkmap import CATEGORY_KEYS
from rer.linkmap.linkmap import ensure_required_root_url
from rer.linkmap.linkmap import is_valid_date
from rer.linkmap.linkmap import is_valid_url
from rer.linkmap.linkmap import today_date_string
from xml.sax.saxutils import escape
from zExceptions import NotFound
from zope.component import getUtility

import os

REGISTRY_PREFIX = "rer.linkmap.controlpanels.settings.ILinkMapSettings"
ROOT_KEY = "amministrazione_trasparente"
# haproxy routes any path ending in "at_map.json"/"at_map.xml" to this same
# view regardless of domain, so redirecting to a path ending the same way
# would loop back here forever. Redirect to a path outside that ACL instead,
# letting Volto render its normal not-found page for it.
DISABLED_VIEW_REDIRECT_PATH = "pagina-non-disponibile"


def get_registry_value(field_name, default=""):
    return api.portal.get_registry_record(
        f"{REGISTRY_PREFIX}.{field_name}",
        default=default,
    )


def get_expose_json():
    return get_registry_value("expose_json", default=True)


def get_expose_xml():
    return get_registry_value("expose_xml", default=True)


def get_frontend_url():
    """Return the public-facing Volto frontend URL.

    Mirrors the fallback chain plone.volto itself uses to build frontend
    URLs (see plone.volto.patches.construct_url): env var, then the
    volto.frontend_domain registry record, falling back to the backend's
    own (possibly VirtualHostBase-rewritten) URL.
    """
    frontend_domain = api.portal.get().absolute_url()
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IVoltoSettings, prefix="volto", check=False)
    settings_frontend_domain = os.environ.get("VOLTO_FRONTEND_DOMAIN") or getattr(
        settings, "frontend_domain", None
    )
    if settings_frontend_domain:
        frontend_domain = settings_frontend_domain
    return frontend_domain.rstrip("/")


def redirect_to_disabled_view(request):
    request.response.redirect(f"{get_frontend_url()}/{DISABLED_VIEW_REDIRECT_PATH}")


def get_data_ultima_modifica():
    value = get_registry_value("data_ultima_modifica")
    if is_valid_date(value):
        return value
    return today_date_string()


def build_category_map_from_fields():
    """Build category map from individual field values."""
    category_map = {}
    for key in CATEGORY_KEYS:
        value = get_registry_value(key)
        if value and is_valid_url(value.strip()):
            category_map[key] = value.strip()
    return category_map


def build_payload():
    data_ultima_modifica = get_data_ultima_modifica()
    category_map = build_category_map_from_fields()
    ensure_required_root_url(category_map, api.portal.get().absolute_url())

    payload = {
        "data_ultima_modifica": data_ultima_modifica,
        CATEGORY_C1: category_map,
    }
    return payload


def build_xml(payload):
    root_open = '<amministrazione_trasparente xmlns="https://guida-servizi.anticorruzione.it/trasparenza">'
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        root_open,
        f"  <data_ultima_modifica>{escape(payload['data_ultima_modifica'])}"
        "</data_ultima_modifica>",
        "  <map>",
    ]

    category = CATEGORY_C1

    lines.append(f"    <{category}>")
    map_values = payload.get(category, {})
    for map_key in CATEGORY_KEYS:
        map_url = map_values.get(map_key)
        if not map_url:
            continue
        lines.append(f"      <{map_key}>{escape(map_url)}</{map_key}>")
    lines.append(f"    </{category}>")
    lines.extend(["  </map>", "</amministrazione_trasparente>"])
    return "\n".join(lines)


class ATMapJSONView(BrowserView):
    def __call__(self):
        if aq_base(self.context) is not aq_base(api.portal.get()):
            raise NotFound()
        if not get_expose_json():
            redirect_to_disabled_view(self.request)
            return ""
        self.request.response.setHeader(
            "Content-Type", "application/json; charset=utf-8"
        )
        payload = build_payload()
        return dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)


class ATMapXMLView(BrowserView):
    def __call__(self):
        if aq_base(self.context) is not aq_base(api.portal.get()):
            raise NotFound()
        if not get_expose_xml():
            redirect_to_disabled_view(self.request)
            return ""
        self.request.response.setHeader(
            "Content-Type", "application/xml; charset=utf-8"
        )
        payload = build_payload()
        return build_xml(payload)
