import datetime as dt

import pytest

import recommender

class TestZip2County:
	"""
	Make sure the lookup from zip code to county FIPS works right
	"""

	def setup_method(self):
		recommender.load()

	@pytest.mark.parametrize("zipcode, expected_county", [
		("02115", {"city": "Boston", "state": "MA", "county_fips": "25025"}),
		("10001", {"city": "New York", "state": "NY", "county_fips": "36061"}),
		("94105", {"city": "San Francisco", "state": "CA", "county_fips": "06075"}),
	])
	def test_valid_zipcodes(self, zipcode, expected_county):
		county = recommender.zip_2_county.get(zipcode)
		assert county == expected_county

	@pytest.mark.parametrize("zipcode", ["00000", "abcde", "12"])
	def test_invalid_zipcodes(self, zipcode):
		county = recommender.zip_2_county.get(zipcode)
		assert county is None



class TestFips2Recs:
	"""
	Make sure the lookup from County FIPS code to country names works
	"""

	def setup_method(self):
		recommender.load()
		assert len(recommender.fips_2_recs) > 0

	@pytest.mark.parametrize("county_fips, expected_recs", [
		("25025", ["HAI", "COL", "BRA"]),
		("36061", ["MEX", "CAN", "KOR"]),
		("06075", ["MEX", "KOR", "CAN"]),
	])
	def test_valid_fips(self, county_fips, expected_recs):
		recs = recommender.fips_2_recs.get(county_fips)
		assert recs == expected_recs

	@pytest.mark.parametrize("county_fips", ["00000", "abcde", "99"])
	def test_invalid_fips(self, county_fips):
		recs = recommender.fips_2_recs.get(county_fips)
		assert recs is None


class TestProcessZipcode:
	"""
	Make sure the full cycle of zipcode to text message works right
	"""

	def setup_method(self):
		recommender.load()

	@pytest.mark.parametrize("zipcode", ["02115", "10001", "94105"])
	def test_valid_zipcodes(self, zipcode):
		msg = recommender.process_zipcode(zipcode)
		assert not msg.startswith("⚠️ Sorry")

	@pytest.mark.parametrize("zipcode", ["00000", "abcde", "12"])
	def test_invalid_zipcodes(self, zipcode):
		msg = recommender.process_zipcode(zipcode)
		assert msg.startswith("⚠️ Sorry")

	def test_full_mesasge(self):
		msg = recommender.process_zipcode("02115")
		assert "02115" in msg
		assert "Boston, MA" in msg
		assert "BRA vs MAR" in msg


class TestAsLocalTime:
	"""
	Make sure UTC game times get converted to local time for the given zipcode
	"""

	def setup_method(self):
		recommender.load()

	def test_converts_to_local_timezone(self):
		game_time_utc = dt.datetime(2026, 6, 11, 20, 0, tzinfo=dt.timezone.utc)
		local_time = recommender._as_local_time("02115", game_time_utc)
		# Boston is America/New_York — EDT in June (UTC-4)
		assert local_time.hour == 16
		assert local_time.utcoffset() == dt.timedelta(hours=-4)

	def test_unknown_zipcode_falls_back_to_utc(self):
		game_time_utc = dt.datetime(2026, 6, 11, 20, 0, tzinfo=dt.timezone.utc)
		local_time = recommender._as_local_time("00000", game_time_utc)
		assert local_time == game_time_utc