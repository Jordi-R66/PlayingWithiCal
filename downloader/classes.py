from __future__ import annotations
from datetime import datetime, timezone, timedelta

from math import floor

def ENT(x: float) -> int:
	return int(floor(x))

class Date(datetime):
	UNIX_EPOCH: datetime = datetime(1970, 1, 1, tzinfo=timezone.utc)

	def __init__(self, dt_object: datetime):
		super.__init__(dt_object.year, dt_object.month, dt_object.day, dt_object.hour, dt_object.minute, tzinfo=dt_object.tzinfo)

	def dayFrac(self) -> float:
		"""Outputs the fraction of the day as a float"""
		H, M = self.hour, self.minute

		if (H >= 24 or M >= 60):
			return float('nan')

		return (H * 60 + M) / 1440.0

	def JulianDay(self, relative: datetime=None) -> float:
		YEAR, MONTH, DAY = self.year, self.month, self.day

		if (MONTH in (1, 2)):
			YEAR -= 1
			MONTH += 12

		S: int = ENT(YEAR / 100)
		B: int = 2 - S + ENT(S / 4)

		JJ: float = ENT(365.25 * YEAR) + ENT(30.6001 * (MONTH + 1)) + DAY + self.dayFrac() + B + 1720994.5

		if (relative != None):
			JJ -= relative.JulianDay(None)

		return JJ

class Event:
	def __init__(self):
		self.start: datetime = None
		self.end: datetime = None

		self.name: str = None
		self.teachers: list[str] = None
		self.groups: list[str] = None
		self.location: str = None

	def getDuration(self) -> timedelta:
		return self.end - self.start

	def readRawDescription(description: str) -> tuple[list[str]]:
		canParse: bool = False

		groups: list[str] = []
		people: list[str] = []

		for l in description.split("\\n"):
			canParse = l not in ("", "A valider")
			canParse = canParse and ("Exported" not in l)

			if canParse:
				if "   " in l:
					split_person_name: tuple[str] = tuple(reversed(l.split("   ")))

					firstname: list[str] = split_person_name[0].split(" ")

					for i in range(len(firstname)):
						firstname[i] = firstname[i].capitalize()

					firstname: str = " ".join(firstname)

					surname: str = split_person_name[1].upper()
					people.append(f"{firstname} {surname}")
				else:
					groups.append(l)

		groups.sort()
		people.sort()

		return groups, people

	def copy(self) -> Event:
		newEvent: Event = Event()

		newEvent.start = self.start
		newEvent.end = self.end

		newEvent.name = str(self.name)
		newEvent.groups = list(self.groups)
		newEvent.teachers = list(self.teachers)
		newEvent.location = list(self.location)

		return newEvent

	def setToLineBlock(self, lines: list[str]) -> None:
		for l in lines:
			split_line = l.split(":")
			key, value = split_line[0], ":".join(split_line[1::])

			if (key.startswith("DT")):
				stamp: str = value
				time_obj: datetime = Event.parseTimeStamp(stamp)

				if ("START" in key):
					self.start = time_obj
				elif ("END" in key):
					self.end = time_obj
			elif (key == "SUMMARY"):
				self.name = str(value)
			elif (key == "LOCATION"):
				locations: list[str] = value.split("\\,")

				self.location = list(locations)
			elif (key == "DESCRIPTION"):
				self.groups, self.teachers = Event.readRawDescription(value)

	def parseTimeStamp(stamp: str) -> datetime:
		"""
		[YYYYMMDD]T[HHmmSS][Z]

		Z represents the timezone, here Z means Zulu which is UTC

		For example 20250920T115117Z

		--> 2025-09-20 @ 11:51:17 UTC
		"""

		split_stamp: tuple[str] = tuple(stamp.split("T"))
		date_string: str = split_stamp[0]
		event_time: str = split_stamp[1]

		time_string: str = event_time[0:6]

		year: int = int(date_string[0:4])
		month: int = int(date_string[4:6])
		day: int = int(date_string[6:8])

		hour: int = int(time_string[0:2])
		minute: int = int(time_string[2:4])
		second: int = int(time_string[4:6])

		output: datetime = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)

		return output

	def __str__(self):
		return f"\t{self.name}\n{"-"*50}\nFROM\t{self.start.astimezone()}\nTO\t{self.end.astimezone()}\n\t({self.getDuration()})\nIN\t{"\n\t".join(self.location)}\nFOR\t{"\n\t".join(self.groups)}\nWITH\t{"\n\t".join(self.teachers)}"