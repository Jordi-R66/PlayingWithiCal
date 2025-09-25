from classes import Event, Date
from datetime import datetime, timezone
from icsmanager import loadRemoteStream, getEventsFromStream, downloadICS

ics_url: str = "https://proseconsult.umontpellier.fr/jsp/custom/modules/plannings/direct_cal.jsp?data=58c99062bab31d256bee14356aca3f2423c0f022cb9660eba051b2653be722c4255dc57febc36bcda019d951db547ac9dc5c094f7d1a811b903031bde802c7f52fd380b992d3771de6139e0d9278c8e91aa43e5f4eeaa642fb89a601c5d38bdbab589f4bd73caa3aaf22c4ddebdb494003799732025a3a02e4d39813a2bcd1c4,1"
now: Date = Date(datetime.now(tz=timezone.utc))

downloadICS(ics_url, "q3.ics")

stream: str = loadRemoteStream(ics_url)
events: list[Event] = getEventsFromStream(stream, now)

print(events[0], sep="\n\n")