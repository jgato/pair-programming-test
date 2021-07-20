from unittest import TestCase

from service.time_converter import iso_format_to_unix_time, time_elapsed_in_hours


class TestTimeConverter(TestCase):

    def test_iso_format_to_unix_time(self):
        self.assertEqual(iso_format_to_unix_time('1970-01-01T00:00:00'), 0)
        self.assertRaises(TypeError, iso_format_to_unix_time, 23434)  # Wrong format
        self.assertRaises(ValueError, iso_format_to_unix_time, '20-05-1979T01:00:01')  # Wrong format
        self.assertEqual(iso_format_to_unix_time('1970-01-01T01:00:01'), 3601)
        self.assertEqual(iso_format_to_unix_time('2020-02-29T23:12:41'), 1583017961)

    def test_calculate_elapsed_time_in_hours_from_two_unix_timestamps(self):
        earlier = iso_format_to_unix_time('2018-05-24T11:30:00')
        later = iso_format_to_unix_time('2018-05-24T12:00:00')

        self.assertEqual(time_elapsed_in_hours(earlier, later), 0.5)