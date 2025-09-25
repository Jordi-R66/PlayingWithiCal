from classes import *
from requests import *
from datetime import datetime

from os import remove

def downloadICS(ics_url: str, ics_file: str) -> None:
	req: Response = get(ics_url)
	req.raise_for_status()

	fp = open(ics_file, "bw")
	fp.write(req.content)
	fp.close()

def openICS(icsFile: str) -> str:
	output: str = None

	fp = open(icsFile, "r", encoding="utf-8")
	output = fp.read()
	fp.close()

	return output

def loadRemoteStream(ics_url: str) -> str:
	downloadICS(ics_url, "temp.ics")
	stream: str = openICS("temp.ics")

	remove("temp.ics")

	return stream

def getEventsFromStream(ics_stream: str, filterDate: datetime | None=None) -> list[Event]:
	ics_lines: list[str] = ics_stream.split("\n")

	lines: list[str] = []
	events: list[Event] = []

	readingEvent: bool = False

	eventObj: Event | None = None

	for l in ics_lines:
		match l:
			case "BEGIN:VEVENT":
				readingEvent = True
				eventObj = Event()
				continue
			case "END:VEVENT":
				readingEvent = False

				eventObj.setToLineBlock(lines)
				if ((filterDate != None) and (eventObj.end >= filterDate)) or (filterDate == None):
					events.append(eventObj.copy())

				eventObj = None

				lines.clear()
				continue

		if (readingEvent):
			if (l[0].isupper()):
				lines.append(l)
			elif (l[0] == " "):
				lines[len(lines) - 1] += l[1::]

	events.sort(key=lambda x: x.start, reverse=False)

	return events

def filterBetween(events: list[Event], from_time: datetime, to_time: datetime) -> list[Event]:
	output: list[Event] = []

	for event in events:
		if event.end >= from_time and event.start <= to_time:
			output.append(event)

	output.sort(key=lambda x: x.start, reverse=False)

	return output