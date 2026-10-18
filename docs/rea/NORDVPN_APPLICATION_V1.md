# REA → Nord VPN application seed v1

Status: BOUNDED_APPLICATION_SEED. Authority: NONE.
NordVPN product reverse engineering: NOT_AUTHORIZED / NOT_PERFORMED.

## Owner direction

Start with REA (morluto/rea, Reverse Engineer Anything) and apply that method
toward the Nord VPN domain. REA remains the method/reference subject. Nord VPN
is a destination domain parameter, not a license to inspect proprietary NordVPN
product bytes without an ownership pin.

## Exact boundary

| Claim | Disposition |
| --- | --- |
| REA method reference pinned | YES — `c12d9eda87aa5a022ee7e18ea96d8d03bfd12e96` |
| Owned Nord VPN domain fixture authorized | YES — `tests/mission/fixtures/owned_nordvpn_surface` |
| Proprietary NordVPN client/binary inspection | NOT_AUTHORIZED |
| Mission rehearsal `domain=nordvpn` on owned fixture | COMPLETE locally (implementer evidence) |
| NordVPN behavioral equivalence | NOT_ESTABLISHED |
| Legal clearance | NOT_ESTABLISHED |
| Independent qualification | NOT_GRANTED |

## Connected path

```text
REA method pin
    → rights gate (RIGHTS_V1.json)
    → admit authorized target only
    → mission inspect/abstract/construct/test/learn
    → reconstruction campaign for owned surface
    → future authorized NordVPN/NordSecurity pin (pending)
```

CLI:

```bash
python3 scripts/mission/nordvpn_application.py validate-rights
python3 scripts/mission/nordvpn_application.py admit --target tests/mission/fixtures/owned_nordvpn_surface
python3 scripts/mission/nordvpn_application.py rehearse \
  --target tests/mission/fixtures/owned_nordvpn_surface \
  --state-root /tmp/oxycok-nordvpn-rehearsal
python3 scripts/reconstruction/campaign.py \
  --census reconstruction/subjects/nordvpn/CENSUS_V1.json \
  audit --campaign reconstruction/subjects/nordvpn/CAMPAIGN_V1.json
```

## Records

- Rights: `reconstruction/subjects/nordvpn/RIGHTS_V1.json`
- Method transfer: `reconstruction/subjects/nordvpn/METHOD_TRANSFER_V1.json`
- Census/campaign/audit: `reconstruction/subjects/nordvpn/`
- Rehearsal evidence: `docs/rea/nordvpn/evidence/OWNED_SURFACE_REHEARSAL_V1.json`
- Real REA host lane: still ENVIRONMENT_BLOCKED per prior evidence; not bypassed

## Next exact action

Owner supplies either (a) an authorized NordVPN/NordSecurity analysis pin with
rights basis and census, or (b) a decision to deepen original OXYCOK VPN-session
contracts from the owned surface without product inspection. Do not point REA at
proprietary NordVPN installs in the meantime.
