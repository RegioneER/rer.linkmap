from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from redturtle.linkmap import _
from redturtle.linkmap.linkmap import CATEGORY_KEYS
from redturtle.linkmap.linkmap import is_valid_date
from redturtle.linkmap.linkmap import is_valid_url
from zope.interface import Interface
from zope.interface import invariant
from zope.interface import Invalid
from zope.schema import SourceText
from zope.schema import TextLine


def _validate_entries(data):
    allowed_keys = set(CATEGORY_KEYS)
    for line in (getattr(data, "entries", "") or "").splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        if "|" not in cleaned:
            raise Invalid(_("invalid_entries_line", default="Each row must be in 'chiave|url' format."))
        key, value = cleaned.split("|", 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            raise Invalid(_("invalid_entries_line", default="Each row must be in 'chiave|url' format."))
        if key not in allowed_keys:
            raise Invalid(_("invalid_entries_key", default="Chiave non valida per la categoria scelta."))
        if not is_valid_url(value):
            raise Invalid(_("invalid_entries_url", default="URL non valido."))


class ILinkMapSettings(Interface):
    data_ultima_modifica = TextLine(
        title=_("data_ultima_modifica_title", default="Data ultima modifica"),
        description=_(
            "data_ultima_modifica_description",
            default="Data in formato GG/MM/AAAA. Se non impostata verra usata la data corrente.",
        ),
        required=False,
        default="",
    )

    entries = SourceText(
        title=_("map_entries_title", default="Mappa link"),
        description=_(
            "map_entries_description",
            default="Una riga per voce nel formato chiave|url. Sono ammesse solo le chiavi dello schema c.1.",
        ),
        required=False,
        default="",
    )

    @invariant
    def validate_map(data):
        value = data.data_ultima_modifica or ""
        if value and not is_valid_date(value):
            raise Invalid(
                _(
                    "invalid_date",
                    default="La data deve essere nel formato GG/MM/AAAA.",
                )
            )
        _validate_entries(data)


class LinkMapControlPanelForm(RegistryEditForm):
    schema = ILinkMapSettings
    id = "redturtle-linkmap-settings"
    label = _(
        "linkmap_controlpanel_title",
        default="Configurazione Link Map Amministrazione Trasparente",
    )


class LinkMapControlPanelView(ControlPanelFormWrapper):
    form = LinkMapControlPanelForm


__all__ = ["ILinkMapSettings", "LinkMapControlPanelForm", "LinkMapControlPanelView"]
