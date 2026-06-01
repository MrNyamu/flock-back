# THIS MODULE POLLS KISMET AND RUNS FLOCK SIGNATURE MATCHING AGAINST ALL SEEN DEVICES


# ETC IMPORTS
import urllib.request, urllib.error, json, base64, time, threading, csv
from datetime import datetime
from pathlib import Path


# NSM IMPORTS
from vars import Variables
from database import DataBase
from signatures import FLOCK_SIGNATURES


# CONSTANTS
console      = Variables.console
KISMET_URL   = "http://127.0.0.1:2501"
KISMET_CONF  = Path.home() / ".kismet" / "kismet_httpd.conf"
POLL_INTERVAL = 2  # seconds between Kismet polls

KISMET_FIELDS = [
    ["kismet.device.base.macaddr",                                                                        "mac"       ],
    ["kismet.device.base.name",                                                                           "name"      ],
    ["kismet.device.base.type",                                                                           "type"      ],
    ["kismet.device.base.signal/kismet.common.signal.last_signal",                                        "rssi"      ],
    ["kismet.device.base.channel",                                                                        "channel"   ],
    ["kismet.device.base.manuf",                                                                          "vendor"    ],
    ["kismet.device.base.crypt_string",                                                                   "encryption"],
    ["kismet.device.base.last_time",                                                                      "last_seen" ],
    ["kismet.device.base.first_time",                                                                     "first_seen"],
    ["kismet.device.base.location/kismet.common.location.avg_loc/kismet.common.location.geopoint",       "geopoint"  ],
    ["kismet.device.base.location/kismet.common.location.avg_loc/kismet.common.location.alt",            "alt"       ],
]

WIGLE_PATH = Path(__file__).parent.parent / "database" / "wigle.csv"
WIGLE_HEADER = ["WigleWifi-1.4,appRelease=2.26,model=Kismet,release=2024,device=Dooku,display=,board=,brand=NSM"]
WIGLE_COLS   = ["MAC","SSID","AuthMode","FirstSeen","Channel","RSSI","CurrentLatitude","CurrentLongitude","AltitudeMeters","AccuracyMeters","Type"]




class Kismet_Watcher():
    """Polls Kismet REST API and runs Flock signature matching on all seen devices"""


    _auth        = None
    _seen        = set()
    _wigle_seen  = set()


    @classmethod
    def _get_auth(cls):
        if cls._auth: return cls._auth

        user, pw = "kismet", "warrig"

        try:
            for line in KISMET_CONF.read_text().splitlines():
                if line.startswith("httpd_username"): user = line.split("=", 1)[1].strip()
                if line.startswith("httpd_password"): pw   = line.split("=", 1)[1].strip()
        except Exception: pass

        token     = base64.b64encode(f"{user}:{pw}".encode()).decode()
        cls._auth = f"Basic {token}"
        return cls._auth


    @classmethod
    def _get_devices(cls):
        try:
            body = json.dumps({"fields": KISMET_FIELDS}).encode()
            req  = urllib.request.Request(
                f"{KISMET_URL}/devices/summary/devices.json",
                data=body,
                method="POST",
                headers={"Authorization": cls._get_auth(), "Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as r:
                data = json.loads(r.read())
                if isinstance(data, dict): data = data.get("devices", [])
                return data
        except Exception:
            return []


    @classmethod
    def _match(cls, device):
        """Check device against Flock signatures — returns match reason or None"""

        mac    = (device.get("mac")    or "").lower()
        name   = (device.get("name")   or "").lower()
        vendor = (device.get("vendor") or "").lower()

        for prefix in FLOCK_SIGNATURES.get("mac_prefixes", []):
            if mac.startswith(prefix.lower()):
                return f"MAC prefix match: {prefix}"

        for pattern in FLOCK_SIGNATURES.get("wifi_ssid_patterns", []):
            if pattern.lower() in name:
                return f"SSID pattern match: {pattern}"

        for pattern in FLOCK_SIGNATURES.get("wifi_ssid_patterns", []):
            if pattern.lower() in vendor:
                return f"Vendor match: {pattern}"

        return None


    @classmethod
    def _push_wigle(cls, device):
        """Append device to wigle.csv for WiGLE upload"""

        geopoint = device.get("geopoint") or []
        lat = geopoint[1] if len(geopoint) > 1 else ""
        lon = geopoint[0] if len(geopoint) > 0 else ""

        first_seen = device.get("first_seen")
        if first_seen:
            first_seen = datetime.utcfromtimestamp(first_seen).strftime("%Y-%m-%d %H:%M:%S")

        row = [
            device.get("mac",        ""),
            device.get("name",       ""),
            device.get("encryption", ""),
            first_seen or "",
            device.get("channel",    ""),
            device.get("rssi",       ""),
            lat,
            lon,
            device.get("alt",        ""),
            "",
            "WIFI",
        ]

        write_header = not WIGLE_PATH.exists()

        with open(WIGLE_PATH, "a", newline="") as f:
            if write_header:
                f.write(WIGLE_HEADER[0] + "\n")
                csv.writer(f).writerow(WIGLE_COLS)
            csv.writer(f).writerow(row)


    @classmethod
    def _poll(cls):
        """get the devices"""


        devices = cls._get_devices()

        for device in devices:
            mac = device.get("mac")
            if not mac: continue

            if mac not in cls._wigle_seen:
                cls._wigle_seen.add(mac)
                cls._push_wigle(device)

            reason = cls._match(device)
            if not reason: continue

            save_data = {
                "mac":        mac,
                "ssid":       device.get("name"),
                "type":       "wifi",
                "rssi":       device.get("rssi"),
                "channel":    device.get("channel"),
                "vendor":     device.get("vendor"),
                "encryption": None,
                "source":     "kismet",
                "time_stamp": time.strftime("%m/%d/%Y  -  %H:%M:%S"),
                "first_seen": device.get("first_seen"),
                "last_seen":  device.get("last_seen"),
            }

            if mac not in cls._seen:
                cls._seen.add(mac)
                console.print(f"[bold red][!] FLOCK HIT (Kismet):[/bold red] [bold yellow]{device.get('name', 'unknown')}[/bold yellow] — {reason}")
                DataBase.push_device(save_data)
            elif Variables.packet:
                console.print(f"[bold cyan][PKT] AI Camera (Kismet):[/bold cyan] [bold yellow]{device.get('name', 'unknown')}[/bold yellow] — {reason}")
                DataBase.push_packet(save_data)


    @classmethod
    def main(cls):
        """Run polling loop in background thread"""


        if not Variables.kismet: return False


        time_start = time.time()
        time_stamp = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
        console.print(f"[bold green]Timestamp:[bold yellow] {time_stamp}\n")

        console.print("[bold green][+][/bold green]  Kismet watcher started — checking every 10s")

        def loop():
            while True:
                try:
                    cls._poll()
                except Exception as e:
                    console.print(f"[bold red][!] Kismet watcher error:[bold yellow] {e}")
                time.sleep(POLL_INTERVAL)

        threading.Thread(target=loop, daemon=True).start()

        if Variables.ble:
            from flock_finder import BLE_Sniffer
            threading.Thread(target=BLE_Sniffer.main, args=(Variables.verbose,), daemon=True).start()
            console.print("[bold green][+][/bold green]  BLE sniffer started")


        while True:
            try:

                if Variables.ifaces:
                    while Variables.BACKGROUND: time.sleep(1)
                else:
                    from server import Web_Server; time.sleep(.4)
                    Web_Server.start()

            except KeyboardInterrupt as e:

                Variables.BACKGROUND = False
                time_duration = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - time_start))

                time.sleep(0.1); console.print(f"\n[bold red][-] Killing Background Threads.....\n")

                total = len(Variables.ble_ai_cameras) + len(Variables.wifi_ai_cameras)

                console.print("[bold red] =====  Found AI Cameras  ===== \n")
                console.print(f"[bold yellow]BLE:[/bold yellow]   {len(Variables.ble_ai_cameras)}")
                console.print(f"[bold yellow]WiFi:[/bold yellow]  {len(Variables.wifi_ai_cameras)}")
                console.print(f"[bold green]Total:[/bold green] {total}\n")

                console.print(f"[bold green]Program Duration:[bold yellow] {time_duration}")
