# Atlas Portainer plugin

Independent, read-only inventory connector for Atlas. Docker environments, Compose stacks, containers, published ports and declared startup dependencies.

## Status

Initial extracted package, version 1.0.0. This repository is public and can be downloaded anonymously through Atlas’s repository installer. The collector implementation already exists in Atlas. Repository installation is separate from migrating an existing bundled connector; do not create a duplicate scheduled collector for the same system.

## Install

1. Open **Sources & settings → Add-ins → Add GitHub repository** in Atlas.
2. Enter `https://github.com/42bios/atlas-plugin-portainer`; optionally pin a release tag or commit.
3. Review the downloaded files and commit. Confirm trust with the exact repository name.
4. Add a connector instance, configure it, then select **Import now**.
5. After checking imported inventory, choose an import schedule if desired.

## Configuration

Set **Portainer URL** to your controller HTTPS address. Enter an API token in the private credential field. For a self-signed certificate, provide its SHA-256 fingerprint; do not disable TLS verification. Container environment variables and credentials are not imported.

Credentials: **API token**. Credentials belong in Atlas's private credential field, never in this repository, issues or screenshots.

## Runtime and limits

Atlas add-in manifest schema 1, connector API 1, Python runtime. Atlas provides per-instance configuration paths and scoped snapshot credentials. This documents inventory; it does not monitor availability or modify the upstream system. Existing manual overrides are retained by stable connector-local IDs.

Repository code runs with Atlas application permissions. Checksums verify the downloaded files, not the author's trustworthiness. Install only code you have reviewed and trust.

## Development

Run `python -m unittest discover -s tests` before publishing. After modifying declared package files, run `python tools/update_manifest.py` and bump `version` in `atlas-addin.json`. Commit all checksum changes together. CI checks file integrity, Python syntax and collector fixtures without contacting a live system.
