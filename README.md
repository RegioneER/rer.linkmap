# rer.linkmap

[![PyPI](https://img.shields.io/pypi/v/rer.linkmap.svg)](https://pypi.org/project/rer.linkmap)
[![Python](https://img.shields.io/pypi/pyversions/rer.linkmap.svg)](https://pypi.org/project/rer.linkmap)
[![Tests](https://github.com/redturtle/rer.linkmap/actions/workflows/tests.yml/badge.svg)](https://github.com/redturtle/rer.linkmap/actions/workflows/tests.yml)
[![License: GPL v2](https://img.shields.io/pypi/l/rer.linkmap.svg)](https://pypi.org/project/rer.linkmap)

Plone add-on to manage and expose the "Amministrazione Trasparente" link map
required by the AGID/ANAC transparency specification.

Links are configured from a control panel and exposed through dedicated Plone
views in JSON and XML format.

Reference specification:
<https://guida-servizi.anticorruzione.it/it/help/trasparenza/amministrazione-trasparente/#la-mappa-dei-link-della-sezione-at>

## Features

- Control panel for configuring all transparency-map URLs.
- Dedicated outputs at portal root:
	- `at_map.json`
	- `at_map.xml`
- Independent flags to enable/disable JSON and XML exposure.
- REST API control panel integration (`linkmap-settings`).

## Requirements

- Plone 6 (tested with Plone 6.2)
- Python 3.10 - 3.13

## Installation

Add `rer.linkmap` to your Plone environment and install it from the Add-ons
control panel.

If you are using a classic buildout-based setup, add it to `eggs`:

```ini
[buildout]
eggs =
		rer.linkmap
```

## Development Setup

This project includes a `Makefile` workflow based on `uv`.

```bash
make install      # create venv, install deps, generate instance config
make start        # start Plone on localhost:8080
make create-site  # create a fresh Plone site
```

Useful commands:

```bash
make test
make test-coverage
make lint
make format
make i18n
```

## Configuration

After installation, configure the add-on in:

- Site Setup -> Link map settings (`linkmap-settings`)

Main options:

- `expose_json`: enable/disable `@@at_map.json`
- `expose_xml`: enable/disable `@@at_map.xml`
- `data_ultima_modifica`: date string in `GG/MM/AAAA`
- one URL field for each transparency section key

If a format is disabled, the corresponding view returns `404 Not Found`.

## Output Endpoints

Endpoints are available only on the portal root context:

- `/at_map.json`
- `/at_map.xml`

### JSON example

```json
{
	"at_art2_bis_c1": {
		"amministrazione_trasparente": "https://www.example.org/amministrazione-trasparente",
		"disposizioni_generali": "https://www.example.org/disposizioni-generali"
	},
	"data_ultima_modifica": "17/06/2026"
}
```

### XML example

```xml
<?xml version="1.0" encoding="utf-8"?>
<amministrazione_trasparente xmlns="https://guida-servizi.anticorruzione.it/trasparenza">
	<data_ultima_modifica>18/06/2026</data_ultima_modifica>
	<map>
		<at_art2_bis_c1>
			<amministrazione_trasparente>https://www.example.org/at</amministrazione_trasparente>
			<accesso_civico>https://www.example.org/accesso-civico</accesso_civico>
		</at_art2_bis_c1>
	</map>
</amministrazione_trasparente>
```

## REST API Integration

The add-on registers a restapi control panel adapter named
`linkmap-settings`, based on the same schema used by the classic control panel.

## Testing

Run tests with:

```bash
make test
```

The suite verifies:

- install/uninstall profile behavior
- control panel registration
- JSON/XML output shape and namespace
- root-only access to views
- enable/disable behavior for exposed formats

## License

This project is licensed under GPL-2.0-only.

## Credits

Developed with the support of [Regione Emilia Romagna](http://www.regione.emilia-romagna.it)

Regione Emilia Romagna supports the [PloneGov initiative](http://www.plonegov.it).

## Authors

This product was developed by **RedTurtle Technology** team.

Generated using [Cookieplone](https://github.com/plone/cookieplone) and
[cookieplone-templates](https://github.com/plone/cookieplone-templates).
