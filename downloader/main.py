from classes import Event
from datetime import datetime, timezone
from icsmanager import loadRemoteStream, getEventsFromStream, downloadICS

ics_url: str = "https://proseconsult.umontpellier.fr/jsp/custom/modules/plannings/direct_cal.jsp?data=58c99062bab31d256bee14356aca3f2423c0f022cb9660eba051b2653be722c4255dc57febc36bcda019d951db547ac9dc5c094f7d1a811b903031bde802c7f52fd380b992d3771de6139e0d9278c8e91aa43e5f4eeaa642fb89a601c5d38bdbab589f4bd73caa3aaf22c4ddebdb494003799732025a3a02e4d39813a2bcd1c4,1"
now: datetime = datetime(2025, 9, 22, 7, tzinfo=timezone.utc)#datetime.now().astimezone()

downloadICS(ics_url, "q3.ics")

stream: str = loadRemoteStream(ics_url)
events: list[Event] = getEventsFromStream(stream, now)

event = events

print(event[-21], sep="\n\n")