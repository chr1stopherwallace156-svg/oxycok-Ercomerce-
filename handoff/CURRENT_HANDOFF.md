# Current handoff — REA → Nord VPN application seed v1

- Agent owner: Cursor cloud agent. Branch: cursor/rea-nordvpn-subject-542a.
- Starting subject: 8885bca (main after PR #4 Elektron merge).
- End subject: commit containing this handoff; verify external Git/PR identity.
- Owner direction: start with REA and use it toward Nord VPN.
- Method reference: REA morluto/rea @ c12d9eda87aa5a022ee7e18ea96d8d03bfd12e96.
- Destination domain: nordvpn. Authority: NONE.
- Added: docs/rea/NORDVPN_APPLICATION_V1.md, docs/rea/nordvpn/**,
  reconstruction/subjects/nordvpn/**, scripts/mission/nordvpn_application.py,
  tests/mission/fixtures/owned_nordvpn_surface/**,
  tests/mission/test_nordvpn_application.py.
- Updated: AGENTS.md, CURRENT_STATE.md, ROADMAP.md, reconstruction/README.md,
  handoff/CURRENT_HANDOFF.md, handoff/HANDOFF_LOG.md.
- Preserved: REA campaign/census, mission runtime, Elektron bridge, Industrial
  read-only posture, prior red REA host-failure evidence.
- Rights: proprietary NordVPN product inspection NOT_AUTHORIZED. Only owned
  fixture tests/mission/fixtures/owned_nordvpn_surface is admitted
  (subject_sha256 3b2232a5be3fe69cf2530c7b9d03a999420d53be151fe9e01aa626762b8ef246).
- Evidence: owned-surface mission rehearsal COMPLETE with claims
  nordvpn_product_reverse_engineering=NOT_PERFORMED; see
  docs/rea/nordvpn/evidence/OWNED_SURFACE_REHEARSAL_V1.json.
- Reconstruction audit: RECONSTRUCTION_OPEN for nordvpn owned-surface subject.
- Validation: run knowledge validate + knowledge/transfer/mission/reconstruction/
  elektron_bridge unittest suites on this branch before merge reliance.
- Limits: no NordVPN product binary/source inspection; real REA CLI still
  environment-blocked; no legal clearance; no independent qualification; planner
  template is not a VPN client.
- Next exact action: owner either (1) supplies an authorized NordVPN/NordSecurity
  pin with rights basis and whole-tree census, or (2) directs deeper original
  OXYCOK VPN-session contracts from the owned surface only.
- Forbidden: mutate Industrial; inspect proprietary NordVPN without a pin;
  bypass REA ownership checks; erase red evidence; treat rehearsal COMPLETE as
  product RE or equivalence; merge/rebase/squash or elevate authority without
  authorization.

Standard configured runtime: scripts/oxycok.py requires a private pinned Elektron snapshot and automatically attaches it to each new mission. Lower-level mission CLI is a standalone diagnostic. Frontdoor source: scripts/oxycok.py; tests: tests/elektron_bridge/test_frontdoor.py. Actual final probe: docs/elektron_transfer/evidence/ACTUAL_B3B_FRONTDOOR_FINAL_V4.json.
