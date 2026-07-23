Changelog
=========


1.0.10 (unreleased)
-------------------

- Nothing changed yet.


1.0.9 (2026-07-23)
------------------

- Reverted the browserlayers addition and the at_map redirect-on-disabled
  fix; these will ship in a later release.
  [fedevancin]
- at_map.json/at_map.xml now return a blank object instead of a 404 when the
  corresponding format is disabled via the controlpanel.
  [fedevancin]


1.0.8 (2026-07-22)
------------------

- Added the browserlayers to the at_map views.
  [fedevancin]
- Fixed a controlpanel translation bug
  [fedevancin]


1.0.7 (2026-06-25)
------------------

- Refactored package for backwards compatibility with old Plone versions.
  [cekk]
