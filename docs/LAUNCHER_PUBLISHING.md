# Launcher publication

CI builds the Cardenza port from source, runs the DSP and shared-NVS checks,
then uploads `dist/cardenza/GLIDE.bin` with its matching
`dist/cardenza/NOTICES.txt`. It never uploads upstream's Cardputer BIN.
See [CARDENZA.md](../CARDENZA.md): this port is v3.4-L5, not upstream's v3.6.

- **Release:** tag a commit containing the Cardenza source with a new numeric
  `vMAJOR.MINOR[.PATCH]` tag. CI uses `release_type=release`; previous versions
  are kept by default. Existing upstream tags do not contain this port.
- **Nightly:** push source changes to branch `nightly`. CI uses
  `release_type=nightly`; the server replaces previous Nightly versions by
  default after verifying the new upload. Create the branch from this fork's
  source-bearing head. Manual Nightly runs also check out `nightly`.
- **Manual:** choose `release_type`, an existing Cardenza tag for Release, and
  optionally `delete_previous`. `default` means Release false / Nightly true;
  explicit true/false is sent to the server as a query parameter.
- **Pull requests:** build and check only; App Tokens are available solely to
  the upload step, which does not run on pull requests.

The single endpoint is `POST /functions/v1/publish`; the multipart body has
`release_type`, `firmware`, and `notices`. CI does not delete previous files,
create GitHub assets, or hold provider keys. GitHub Contents permission is read.
The server verifies the App/target/repository scope, source commit, image,
size, SHA-256 and public Range download before changing catalog entries.
Release and Nightly both use GitHub as primary download and CDN as backup;
devices list Nightly under **Pre-release**.

One-time setup: authorize this fork as a publication repository for GLIDE,
configure a repository-scoped GitHub upload credential on the server, and set
the permanent Cardenza-scoped GLIDE App Token as `LAUNCHER_APP_TOKEN` in this
repository's Actions Secrets. No Supabase or Bunny master key goes into App CI.
Until this is configured, builds can be checked locally/on pull requests but
upload jobs fail without publishing. This repository change does not claim
that those credentials or a new live publication are already configured.

The backend's scheduled importer still checks upstream stable releases and
does not import Nightly. The inherited download-statistics workflow is limited
to upstream, so it does not add daily commits to this community fork.
