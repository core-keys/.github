<p align="center">
  <img src="https://raw.githubusercontent.com/core-keys/.github/main/brand/banner.png" alt="core-keys — split-key authenticator" width="800">
</p>

A **split-key hardware authenticator for SSH and FIDO2**: the desktop daemon and
a dedicated hardware device must both participate in every authentication, and
the device explicitly approves each use on its own button and display.

The invariant everything here serves: *the device signs only when it has an
authenticated in-session request from the paired desktop, over the exact bytes
to be signed, AND the user presses the button after reading honest context on
the display.*

The display is the security boundary, not the button. The button approves *a*
signature; only the display makes it *the* signature.

## Repositories

| repo | what |
|---|---|
| [spec](https://github.com/core-keys/spec) | the source of truth: frozen design decisions and the section-numbered co-authorization wire protocol |
| [protocol](https://github.com/core-keys/protocol) | `corekeys-protocol` — shared `no_std` Rust crate: CKVP framing, pairing SAS, CBOR record types |
| [daemon](https://github.com/core-keys/daemon) | `corekeys-daemon` — ssh-agent front end, Noise session owner, FIDO2 co-authorization policy |
| [mule-esp32s3](https://github.com/core-keys/mule-esp32s3) | ESP-IDF firmware for the protocol mule, a LilyGO T-Display-S3 |
| [case-tdisplay-s3](https://github.com/core-keys/case-tdisplay-s3) | slide-in 3D-printed case for the board |

The wire is deliberately implemented twice — once in Rust in `protocol`, once in
C in `mule-esp32s3` — so a change to it is always a two-sided edit.

## Status

Design frozen (2026-08-28); M1, mule bring-up, in progress. **Nothing here is
fit for real credentials yet.** The prototype knowingly ships a plaintext
control path for the reflash loop, and the threat claims in `spec/DESIGN.md` are
written to be honest about exactly that.

Everything we wrote is dual-licensed MIT OR Apache-2.0.
