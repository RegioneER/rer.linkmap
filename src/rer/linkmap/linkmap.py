from datetime import date
from zope.schema import URI
from zope.schema.interfaces import InvalidURI

import re

CATEGORY_C1 = "at_art2_bis_c1"
ROOT_KEY = "amministrazione_trasparente"

CATEGORY_KEYS = (
    "amministrazione_trasparente",
    "disposizioni_generali",
    "consulenti_collaboratori",
    "bandi_di_concorso",
    "enti_controllati",
    "sovvenzioni",
    "beni_immobili",
    "opere_pubbliche",
    "organizzazione",
    "personale",
    "performance",
    "attivita_e_procedimenti",
    "bandi_gara_e_contratti",
    "bilanci",
    "controlli_e_rilievi",
    "pagamenti",
    "altri_contenuti",
    "provvedimenti",
    "servizi_erogati",
    "informazioni_ambientali",
    "interventi_straordinari",
    "pianificazione_governo_territorio",
    "strutture_sanitarie_accreditate",
    "atti_generali",
    "rischi_corruttivi_e_trasparenza",
    "piano_integrato_attivita_organizzazione",
    "piano_triennale_prevenzione_corruzione_e_trasparenza",
    "titolari_incarichi_collaborazione_consulenza",
    "enti_diritto_privato_controllati",
    "rappresentazione_grafica",
    "societa_partecipate",
    "criteri_e_modalita",
    "atti_di_concessione",
    "patrimonio_immobiliare",
    "canoni_locazione_o_affitto",
    "tempi_costi_opere_pubbliche",
    "atti_programmazione_opere_pubbliche",
    "organi_di_indirizzo_politico_amministativo",
    "telefono_e_posta_elettronica",
    "sanzioni_mancata_comunicazione_dati",
    "articolazione_uffici",
    "incarichi_amministrativi_di_vertice",
    "dirigenti_cessati",
    "incarichi_conferiti_e_autorizzati_ai_dipendenti",
    "contrattazione_integrativa",
    "titolari_incarichi_dirigenziali_non_generali",
    "dotazione_organica",
    "tassi_di_assenza",
    "contrattazione_collettiva",
    "ammontare_complessivo_dei_premi",
    "dati_relativi_ai_premi",
    "tipologie_di_procedimento",
    "bilancio_preventivo_e_consuntivo",
    "budget",
    "nuclei_di_valutazione",
    "corte_dei_conti",
    "organi_revisione_amministrativa_e_contabile",
    "dati_sui_pagamenti",
    "tempestivita_dei_pagamenti",
    "IBAN_e_pagamenti_informatici",
    "prevenzione_della_corruzione",
    "accessibilita_e_catalogo_dati",
    "accesso_civico",
    "dati_ulteriori",
    "provvedimenti_organo_indirizzo_politico",
    "provvedimenti_dirigenti_amministrativi",
    "servizi_e_standard_di_qualita",
    "costi_contabilizzati",
    "servizi_in_rete",
    "class_action",
    "liste_di_attesa",
)

DATE_RE = re.compile(r"^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/([2]\d{3})$")
URL_FIELD = URI(required=False)


def is_valid_date(value):
    return bool(value and DATE_RE.fullmatch(value))


def today_date_string():
    return date.today().strftime("%d/%m/%Y")


def is_valid_url(value):
    if not value:
        return False
    try:
        URL_FIELD.validate(value.strip())
    except InvalidURI:
        return False
    return True


def allowed_keys():
    return set(CATEGORY_KEYS)


def parse_entries(raw_value):
    lines = (raw_value or "").splitlines()
    pairs = []
    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue
        if "|" not in cleaned:
            raise ValueError(f"Invalid line format: {cleaned}")
        key, url = cleaned.split("|", 1)
        key = key.strip()
        url = url.strip()
        if not key or not url:
            raise ValueError(f"Invalid line format: {cleaned}")
        pairs.append((key, url))
    return pairs


def build_category_map(raw_entries):
    key_values = {}
    allowed = allowed_keys()
    for key, url in parse_entries(raw_entries):
        if key not in allowed:
            continue
        if not is_valid_url(url):
            continue
        key_values[key] = url
    return key_values


def ensure_required_root_url(category_map, fallback_url):
    if category_map.get(ROOT_KEY):
        return
    category_map[ROOT_KEY] = fallback_url
