# Flock Safety — LTE Connectivity

## Overview

Flock cameras transmit data (plate images, metadata) over LTE cellular — it is the primary and default connectivity method. WiFi is secondary, used for installation and field troubleshooting only. The camera does not hop LTE channels; frequency assignment is fully controlled by the tower.

## How LTE Channels Work

LTE bands are subdivided into **resource blocks (RBs)** — 180 kHz chunks the tower dynamically allocates across devices sharing a cell. The specific center frequency within a band is identified by an **EARFCN** (E-UTRA Absolute Radio Frequency Channel Number). The device has no say in which resource blocks it uses — the tower assigns them.

The only frequency changes a Flock camera undergoes:
- **Handover** — tower hands off to a neighboring cell when signal degrades (network-controlled)
- **Band fallback** — negotiates down to a lower band if the preferred one isn't available (network-controlled)

## Frequency Rule

Higher frequency = shorter range, higher capacity.
Lower frequency = longer range, better penetration through structures.

For a solar-powered roadside device with low throughput needs (just uploading images), the network will preference low bands (700–850 MHz) for maximum range and minimal power cost.

## Older Cameras — NimbeLink Skywire HL7648 (LTE Cat-1)

Carriers: **AT&T, T-Mobile**

| Band | Name            | Uplink          | Downlink        |
|------|-----------------|-----------------|-----------------|
| B2   | 1900 MHz        | 1850–1910 MHz   | 1930–1990 MHz   |
| B4   | AWS 1700        | 1710–1755 MHz   | 2110–2155 MHz   |
| B5   | 850 MHz         | 824–849 MHz     | 869–894 MHz     |
| B17  | 700 MHz Lower B | 704–716 MHz     | 734–746 MHz     |

## Newer Cameras — Sierra Wireless RC7611 (LTE Cat-4)

Carriers: **AT&T, T-Mobile, Verizon**

| Band | Name            | Uplink          | Downlink        |
|------|-----------------|-----------------|-----------------|
| B2   | 1900 MHz        | 1850–1910 MHz   | 1930–1990 MHz   |
| B4   | AWS 1700        | 1710–1755 MHz   | 2110–2155 MHz   |
| B5   | 850 MHz         | 824–849 MHz     | 869–894 MHz     |
| B12  | 700 MHz Lower A | 698–716 MHz     | 728–746 MHz     |
| B13  | 700 MHz Upper C | 746–756 MHz     | 777–787 MHz     |
| B14  | FirstNet        | 788–798 MHz     | 758–768 MHz     |
| B66  | AWS-3           | 1710–1780 MHz   | 2110–2200 MHz   |
| B71  | 600 MHz         | 663–698 MHz     | 617–652 MHz     |

## Band 14 — FirstNet

Band 14 is AT&T's dedicated public safety network (FirstNet). The RC7611 explicitly supports it. Given that Flock's primary customer base is law enforcement, this is likely intentional — Flock cameras on newer hardware may be running on the same dedicated public safety spectrum as police radios and dispatch systems.

## Most Likely Operating Band

B17/B12 (700 MHz) for older and newer cameras respectively. 700 MHz offers the longest range and best building penetration, which matches the deployment profile — roadside, solar-powered, low throughput, wide coverage area.
