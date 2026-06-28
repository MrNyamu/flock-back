# References & Sources

## Hardware & Technical Specs

- [CEHRP — Dissection of Flock Safety Camera](https://www.cehrp.org/dissection-of-flock-safety-camera/)
  Physical teardown identifying internal components: NimbeLink Skywire LTE modem, LITE-ON WCBN3510A WiFi/BLE module, GPS module, battery.

- [LITE-ON WCBN3510A FCC Filing](https://fcc.report/FCC-ID/PPQ-WCBN3510A)
  FCC certification for the 802.11 a/b/g/n/ac + BT 4.2 LE combo module used in Flock cameras.

- [NimbeLink Skywire HL7648 FCC Filing](https://fcc.report/FCC-ID/N7NHL7648)
  FCC certification for the LTE Cat-1 modem (older camera hardware).

- [NimbeLink Skywire S7648 Datasheet](https://nimbelink.com/Documentation/Skywire/4G_LTE_Cat_1_SierraWireless/1001720_NL-SW-LTE-S7648_Datasheet.pdf)
  LTE band support for older cameras: B2, B4, B5, B17.

- [Sierra Wireless RC7611 Datasheet](https://www.getwirelessllc.com/wp-content/uploads/2023/10/SierraWireless_RC7611_DataSheet.pdf)
  LTE band support for Falcon V2 cameras: B2, B4, B5, B12, B13, B14, B66, B71.

- [Sierra Wireless RC76B FCC Filing](https://fccid.io/N7NRC76B)
  FCC certification for the RC7611 modem used in newer Flock Falcon V2 cameras.

## Security Research

- [GainSec — Button Presses to Wireless RCE](https://gainsec.com/2025/09/27/button-presses-to-shell-on-flock-safety-license-plate-cameras-over-wi-fi/)
  Initial disclosure: button sequence creates open WiFi AP, hardcoded password, ADB enabled, root shell in under 60 seconds.

- [SimeonOnSecurity — Flock Safety Camera Security Vulnerabilities Research 2026](https://simeononsecurity.com/articles/flock-safety-camera-security-vulnerabilities-research-2026/)
  Comprehensive summary of 51 findings across all Flock hardware. Covers hardcoded SSIDs, unencrypted runtime data, exposed API keys, public camera feeds, Android Things EOL OS, researcher retaliation.

- [Privacy Guides — Ben Jordan Exposes Severe Security Vulnerabilities](https://www.privacyguides.org/news/2025/11/17/ben-jordan-exposes-severe-security-vulnerabilities-in-flock-surveillance-cameras/)
  Ben Jordan's documented demonstrations including 60+ publicly exposed live feeds findable via Google search.

- [GainSec White Paper (Zenodo)](https://zenodo.org/doi/10.5281/zenodo.17584876)
  Full 51-finding white paper by Jon Gaines (GainSec). 22 CVEs assigned, 8 pending.

- [GainSec Research Repo](https://github.com/GainSec/anti-crime-ecosystem-research)
  Raw research artifacts and supporting materials.

## LTE Connectivity Confirmation

- [CEHRP — Dissection of Flock Safety Camera](https://www.cehrp.org/dissection-of-flock-safety-camera/)
  Physical teardown confirms LTE modem (NimbeLink Skywire) inside the camera. Flock cameras transmit over LTE cellular — this is hardware-confirmed, not a claim.

- [Flock Safety — Technical Specifications](https://www.flocksafety.com/product/technical-specifications)
  Flock themselves state cameras are LTE-connected. Confirms cellular as primary connectivity method.

- [NimbeLink Skywire S7648 Datasheet](https://nimbelink.com/Documentation/Skywire/4G_LTE_Cat_1_SierraWireless/1001720_NL-SW-LTE-S7648_Datasheet.pdf)
  Confirms supported LTE bands for older cameras (B2, B4, B5, B17). Note: band support ≠ observed field usage — no public field capture data exists confirming which band Flock cameras actively use.

- [Sierra Wireless RC7611 Datasheet](https://www.getwirelessllc.com/wp-content/uploads/2023/10/SierraWireless_RC7611_DataSheet.pdf)
  Confirms supported LTE bands for Falcon V2 cameras (B2, B4, B5, B12, B13, B14, B66, B71). Same caveat as above.

## LTE Frequency Reference

- [LTE Frequency Bands — Wikipedia](https://en.wikipedia.org/wiki/LTE_frequency_bands)
  Full band table with uplink/downlink ranges for all LTE bands.

- [LTE Band 17 — everythingRF](https://www.everythingrf.com/tech-resources/lte-bands/lte-band-17)
  Band 17 (700 MHz Lower B): UL 704–716 MHz, DL 734–746 MHz.

- [LTE Band 66 — everythingRF](https://www.everythingrf.com/tech-resources/lte-bands/lte-band-66)
  Band 66 (AWS-3): UL 1710–1780 MHz, DL 2110–2200 MHz.

## Camera Spotting & Field Research

- [Ryan Ohoro — Spotting Flock Safety's Falcon Cameras](https://www.ryanohoro.com/post/spotting-flock-safety-s-falcon-cameras)
  Field guide for visually identifying Flock cameras in the wild.
