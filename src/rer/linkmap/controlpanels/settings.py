from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from rer.linkmap import _
from rer.linkmap.linkmap import is_valid_date
from zope.interface import Interface
from zope.interface import invariant
from zope.interface import Invalid
from zope.schema import Bool
from zope.schema import TextLine
from zope.schema import URI


def _category_field(key):
    return URI(
        title=_(
            f"{key}_title",
            default=key.replace("_", " ").title(),
        ),
        description=_(
            f"{key}_description",
            default="Inserisci l'url per questo dato",
        ),
        required=False,
    )


class ILinkMapSettings(Interface):
    expose_json = Bool(
        title=_("expose_json_title", default="Esponi vista JSON"),
        description=_(
            "expose_json_description",
            default="Se selezionato, la mappa dei link sarà disponibile nel "
            "formato JSON.",
        ),
        required=False,
        default=True,
    )

    expose_xml = Bool(
        title=_("expose_xml_title", default="Esponi vista XML"),
        description=_(
            "expose_xml_description",
            default="Se selezionato, la mappa dei link sarà disponibile nel "
            "formato XML.",
        ),
        required=False,
        default=True,
    )

    data_ultima_modifica = TextLine(
        title=_("data_ultima_modifica_title", default="Data ultima modifica"),
        description=_(
            "data_ultima_modifica_description",
            default="Data in formato GG/MM/AAAA. Se non impostata verra usata "
            "la data corrente.",
        ),
        required=False,
        default="",
    )

    amministrazione_trasparente = _category_field("amministrazione_trasparente")
    disposizioni_generali = _category_field("disposizioni_generali")
    consulenti_collaboratori = _category_field("consulenti_collaboratori")
    bandi_di_concorso = _category_field("bandi_di_concorso")
    enti_controllati = _category_field("enti_controllati")
    sovvenzioni = _category_field("sovvenzioni")
    beni_immobili = _category_field("beni_immobili")
    opere_pubbliche = _category_field("opere_pubbliche")
    organizzazione = _category_field("organizzazione")
    personale = _category_field("personale")
    performance = _category_field("performance")
    attivita_e_procedimenti = _category_field("attivita_e_procedimenti")
    bandi_gara_e_contratti = _category_field("bandi_gara_e_contratti")
    bilanci = _category_field("bilanci")
    controlli_e_rilievi = _category_field("controlli_e_rilievi")
    pagamenti = _category_field("pagamenti")
    altri_contenuti = _category_field("altri_contenuti")
    provvedimenti = _category_field("provvedimenti")
    servizi_erogati = _category_field("servizi_erogati")
    informazioni_ambientali = _category_field("informazioni_ambientali")
    interventi_straordinari = _category_field("interventi_straordinari")
    pianificazione_governo_territorio = _category_field(
        "pianificazione_governo_territorio"
    )
    strutture_sanitarie_accreditate = _category_field("strutture_sanitarie_accreditate")
    atti_generali = _category_field("atti_generali")
    rischi_corruttivi_e_trasparenza = _category_field("rischi_corruttivi_e_trasparenza")
    piano_integrato_attivita_organizzazione = _category_field(
        "piano_integrato_attivita_organizzazione"
    )
    piano_triennale_prevenzione_corruzione_e_trasparenza = _category_field(
        "piano_triennale_prevenzione_corruzione_e_trasparenza"
    )
    titolari_incarichi_collaborazione_consulenza = _category_field(
        "titolari_incarichi_collaborazione_consulenza"
    )
    enti_diritto_privato_controllati = _category_field(
        "enti_diritto_privato_controllati"
    )
    rappresentazione_grafica = _category_field("rappresentazione_grafica")
    societa_partecipate = _category_field("societa_partecipate")
    criteri_e_modalita = _category_field("criteri_e_modalita")
    atti_di_concessione = _category_field("atti_di_concessione")
    patrimonio_immobiliare = _category_field("patrimonio_immobiliare")
    canoni_locazione_o_affitto = _category_field("canoni_locazione_o_affitto")
    tempi_costi_opere_pubbliche = _category_field("tempi_costi_opere_pubbliche")
    atti_programmazione_opere_pubbliche = _category_field(
        "atti_programmazione_opere_pubbliche"
    )
    organi_di_indirizzo_politico_amministativo = _category_field(
        "organi_di_indirizzo_politico_amministativo"
    )
    telefono_e_posta_elettronica = _category_field("telefono_e_posta_elettronica")
    sanzioni_mancata_comunicazione_dati = _category_field(
        "sanzioni_mancata_comunicazione_dati"
    )
    articolazione_uffici = _category_field("articolazione_uffici")
    incarichi_amministrativi_di_vertice = _category_field(
        "incarichi_amministrativi_di_vertice"
    )
    dirigenti_cessati = _category_field("dirigenti_cessati")
    incarichi_conferiti_e_autorizzati_ai_dipendenti = _category_field(
        "incarichi_conferiti_e_autorizzati_ai_dipendenti"
    )
    contrattazione_integrativa = _category_field("contrattazione_integrativa")
    titolari_incarichi_dirigenziali_non_generali = _category_field(
        "titolari_incarichi_dirigenziali_non_generali"
    )
    dotazione_organica = _category_field("dotazione_organica")
    tassi_di_assenza = _category_field("tassi_di_assenza")
    contrattazione_collettiva = _category_field("contrattazione_collettiva")
    ammontare_complessivo_dei_premi = _category_field("ammontare_complessivo_dei_premi")
    dati_relativi_ai_premi = _category_field("dati_relativi_ai_premi")
    tipologie_di_procedimento = _category_field("tipologie_di_procedimento")
    bilancio_preventivo_e_consuntivo = _category_field(
        "bilancio_preventivo_e_consuntivo"
    )
    budget = _category_field("budget")
    nuclei_di_valutazione = _category_field("nuclei_di_valutazione")
    corte_dei_conti = _category_field("corte_dei_conti")
    organi_revisione_amministrativa_e_contabile = _category_field(
        "organi_revisione_amministrativa_e_contabile"
    )
    dati_sui_pagamenti = _category_field("dati_sui_pagamenti")
    tempestivita_dei_pagamenti = _category_field("tempestivita_dei_pagamenti")
    IBAN_e_pagamenti_informatici = _category_field("IBAN_e_pagamenti_informatici")
    prevenzione_della_corruzione = _category_field("prevenzione_della_corruzione")
    accessibilita_e_catalogo_dati = _category_field("accessibilita_e_catalogo_dati")
    accesso_civico = _category_field("accesso_civico")
    dati_ulteriori = _category_field("dati_ulteriori")
    provvedimenti_organo_indirizzo_politico = _category_field(
        "provvedimenti_organo_indirizzo_politico"
    )
    provvedimenti_dirigenti_amministrativi = _category_field(
        "provvedimenti_dirigenti_amministrativi"
    )
    servizi_e_standard_di_qualita = _category_field("servizi_e_standard_di_qualita")
    costi_contabilizzati = _category_field("costi_contabilizzati")
    servizi_in_rete = _category_field("servizi_in_rete")
    class_action = _category_field("class_action")
    liste_di_attesa = _category_field("liste_di_attesa")

    @invariant
    def validate_map(data):
        """Validate the control panel settings."""
        value = data.data_ultima_modifica or ""
        if value and not is_valid_date(value):
            raise Invalid(
                _(
                    "invalid_date",
                    default="La data deve essere nel formato GG/MM/AAAA.",
                )
            )


class LinkMapControlPanelForm(RegistryEditForm):
    schema = ILinkMapSettings
    id = "redturtle-linkmap-settings"
    label = _(
        "linkmap_controlpanel_title",
        default=" Configurazione Link Map",
    )


class LinkMapControlPanelView(ControlPanelFormWrapper):
    form = LinkMapControlPanelForm


__all__ = ["ILinkMapSettings", "LinkMapControlPanelForm", "LinkMapControlPanelView"]
