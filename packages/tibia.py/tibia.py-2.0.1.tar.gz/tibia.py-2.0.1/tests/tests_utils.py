import datetime
import unittest

import tibiapy

from tests.tests_tibiapy import TestCommons
from tibiapy import enums, utils

TIBIA_DATETIME_CEST = "Jul 10 2018, 07:13:32 CEST"
TIBIA_DATETIME_CET = "Jan 10 2018, 07:13:32 CET"
TIBIA_DATETIME_PST = "Aug 10 2015, 23:13:32 PST"
TIBIA_DATETIME_INVALID = "13:37:00 10 Feb 2003"

TIBIA_DATE = "Jun 20 2018"
TIBIA_FULL_DATE = "July 23, 2015"
TIBIA_DATE_INVALID = "8 Nov 2018"

TIBIADATA_DATETIME_CET = {
    "date": "2017-11-03 18:34:13.000000",
    "timezone_type": 2,
    "timezone": "CET"
}
TIBIADATA_DATETIME_CEST = {
    "date": "2010-10-05 10:24:18.000000",
    "timezone_type": 2,
    "timezone": "CEST"
}
TIBIADATA_DATETIME_PST = {
    "date": "2015-01-03 20:04:01.000000",
    "timezone_type": 2,
    "timezone": "PST"
}
TIBIADATA_DATE = "2018-12-20"


class TestUtils(TestCommons, unittest.TestCase):
    def testSerializableGetItem(self):
        # Class inherits from Serializable
        world = tibiapy.World("Calmera")

        # Serializable allows accessing attributes like a dictionary
        self.assertEqual(world.name, world["name"])
        # And setting values too
        world["location"] = tibiapy.enums.WorldLocation.NORTH_AMERICA
        self.assertEqual(world.location, tibiapy.enums.WorldLocation.NORTH_AMERICA)

        # Accessing via __get__ returns KeyError instead of AttributeError to follow dictionary behaviour
        with self.assertRaises(KeyError):
            _level = world["level"]  # NOSONAR

        # Accessing an undefined attribute that is defined in __slots__ returns `None` instead of raising an exception.
        del world.location
        self.assertIsNone(world["location"])

        # New attributes can't be created by assignation
        with self.assertRaises(KeyError):
            world["custom"] = "custom value"

    def testTibiaDateTime(self):
        time = utils.parse_tibia_datetime(TIBIA_DATETIME_CEST)
        self.assertIsInstance(time, datetime.datetime)
        self.assertEqual(time.month, 7)
        self.assertEqual(time.day, 10)
        self.assertEqual(time.year, 2018)
        self.assertEqual(time.hour, 5)
        self.assertEqual(time.minute, 13)
        self.assertEqual(time.second, 32)

        time = utils.parse_tibia_datetime(TIBIA_DATETIME_CET)
        self.assertIsInstance(time, datetime.datetime)
        self.assertEqual(time.month, 1)
        self.assertEqual(time.day, 10)
        self.assertEqual(time.year, 2018)
        self.assertEqual(time.hour, 6)
        self.assertEqual(time.minute, 13)
        self.assertEqual(time.second, 32)

    def testTibiaDateInvalidTimezone(self):
        time = utils.parse_tibia_datetime(TIBIA_DATETIME_PST)
        self.assertIsNone(time)

    def testTibiaDateTimeInvalid(self):
        time = utils.parse_tibia_datetime(TIBIA_DATETIME_INVALID)
        self.assertIsNone(time)

    def testTibiaDate(self):
        date = utils.parse_tibia_date(TIBIA_DATE)
        self.assertIsInstance(date, datetime.date)
        self.assertEqual(date.month, 6)
        self.assertEqual(date.day, 20)
        self.assertEqual(date.year, 2018)

    def testTibiaFullDate(self):
        date = utils.parse_tibia_full_date(TIBIA_FULL_DATE)
        self.assertIsInstance(date, datetime.date)
        self.assertEqual(date.month, 7)
        self.assertEqual(date.day, 23)
        self.assertEqual(date.year, 2015)

    def testTibiaDateInvalid(self):
        date = utils.parse_tibia_date(TIBIA_DATETIME_INVALID)
        self.assertIsNone(date)

    def testTibiaDataDatetime(self):
        date = utils.parse_tibiadata_datetime(TIBIADATA_DATETIME_CET)
        self.assertIsInstance(date, datetime.datetime)

        date = utils.parse_tibiadata_datetime(TIBIADATA_DATETIME_CEST)
        self.assertIsInstance(date, datetime.datetime)

        date = utils.parse_tibiadata_datetime(TIBIADATA_DATETIME_PST)
        self.assertIsNone(date)

        # noinspection PyTypeChecker
        # Purposely providing wrong type.
        date = utils.parse_tibiadata_datetime(TIBIA_DATE)
        self.assertIsNone(date)

    def testTryDate(self):
        date = utils.try_date(datetime.datetime.now())
        self.assertIsInstance(date, datetime.date)

        date = utils.try_date(datetime.date.today())
        self.assertIsInstance(date, datetime.date)
        self.assertEqual(date, datetime.date.today())

        date = utils.try_date(TIBIA_DATE)
        self.assertIsInstance(date, datetime.date)

        date = utils.try_date(TIBIA_FULL_DATE)
        self.assertIsInstance(date, datetime.date)

        date = utils.try_date(TIBIADATA_DATE)
        self.assertIsInstance(date, datetime.date)

    def testTryDateTime(self):
        date_time = utils.try_datetime(datetime.datetime.now())
        self.assertIsInstance(date_time, datetime.datetime)

        date_time = utils.try_datetime(TIBIA_DATETIME_CEST)
        self.assertIsInstance(date_time, datetime.datetime)

        date_time = utils.try_datetime(TIBIADATA_DATETIME_CET)
        self.assertIsInstance(date_time, datetime.datetime)

    def testParseNumberWords(self):
        self.assertEqual(utils.parse_number_words("one"), 1)
        self.assertEqual(utils.parse_number_words("..."), 0)
        self.assertEqual(utils.parse_number_words("twenty-one"), 21)
        self.assertEqual(utils.parse_number_words("one hundred two"), 102)
        self.assertEqual(utils.parse_number_words("two thousand forty five"), 2045)

    def testTryEnum(self):
        self.assertEqual(utils.try_enum(enums.Sex, "male"), enums.Sex.MALE)
        self.assertEqual(utils.try_enum(enums.TransferType, "", enums.TransferType.REGULAR), enums.TransferType.REGULAR)
        self.assertEqual(utils.try_enum(enums.WorldLocation, enums.WorldLocation.EUROPE), enums.WorldLocation.EUROPE)

    def testEnumStr(self):
        self.assertEqual(str(enums.Sex.MALE), enums.Sex.MALE.value)
        self.assertEqual(enums.VocationFilter.from_name("royal paladin"), enums.VocationFilter.PALADINS)
        self.assertEqual(enums.VocationFilter.from_name("unknown"), enums.VocationFilter.ALL)
        self.assertIsNone(enums.VocationFilter.from_name("unknown", False))
