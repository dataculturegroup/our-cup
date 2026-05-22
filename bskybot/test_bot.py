import pytest

import bot


class TestBuildRichText:
	"""
	Make sure build_rich_text wraps URLs as link facets so Bluesky renders them as clickable links
	"""

	def test_url_only(self):
		url = "https://example.com/foo"
		tb = bot.build_rich_text(url)
		built_text = tb.build_text()
		assert built_text == url
		facets = tb.build_facets()
		assert len(facets) == 1
		facet = facets[0]
		assert facet.features[0].uri == url
		# byte indexes should slice the url back out of the built text
		built_bytes = built_text.encode("utf-8")
		assert built_bytes[facet.index.byte_start:facet.index.byte_end].decode("utf-8") == url

	def test_url_in_middle(self):
		url = "https://example.com/foo"
		text = f"Check out {url} for more info"
		tb = bot.build_rich_text(text)
		built_text = tb.build_text()
		assert built_text == text
		facets = tb.build_facets()
		assert len(facets) == 1
		facet = facets[0]
		assert facet.features[0].uri == url
		built_bytes = built_text.encode("utf-8")
		assert built_bytes[facet.index.byte_start:facet.index.byte_end].decode("utf-8") == url
		# explicit offsets: "Check out " is 10 bytes (ASCII), url follows
		assert facet.index.byte_start == 10
		assert facet.index.byte_end == 10 + len(url.encode("utf-8"))

	def test_url_after_flag_emojis(self):
		# flag emojis are 8 bytes each in UTF-8 (pair of 4-byte regional indicators),
		# so byte offsets diverge from character offsets — make sure the facet still
		# slices the url back out correctly.
		url = "https://example.com/foo"
		text = f"Fans cheering for 🇧🇷 🇲🇽 🇨🇦 — see {url}"
		tb = bot.build_rich_text(text)
		built_text = tb.build_text()
		assert built_text == text
		facets = tb.build_facets()
		assert len(facets) == 1
		facet = facets[0]
		assert facet.features[0].uri == url
		# the byte indexes must point at the url inside the *original* utf-8 bytes
		text_bytes = text.encode("utf-8")
		assert text_bytes[facet.index.byte_start:facet.index.byte_end].decode("utf-8") == url
		# and they should be byte offsets, not character offsets
		assert facet.index.byte_start == text.encode("utf-8").index(url.encode("utf-8"))
		assert facet.index.byte_start != text.index(url)

	def test_no_url(self):
		text = "Just some plain text with no links"
		tb = bot.build_rich_text(text)
		assert tb.build_text() == text
		assert tb.build_facets() == []

	@pytest.mark.parametrize("text, expected_uri, expected_built_text", [
		# trailing period stripped from uri but kept in the text
		("Visit https://example.com.", "https://example.com", "Visit https://example.com."),
		# trailing comma
		("See https://example.com, then go", "https://example.com", "See https://example.com, then go"),
		# trailing exclamation
		("Check https://example.com!", "https://example.com", "Check https://example.com!"),
		# unmatched closing paren stripped
		("(see https://example.com)", "https://example.com", "(see https://example.com)"),
		# trailing punctuation AFTER an unmatched paren — both stripped
		("(see https://example.com).", "https://example.com", "(see https://example.com)."),
	])
	def test_strips_trailing_punctuation(self, text, expected_uri, expected_built_text):
		tb = bot.build_rich_text(text)
		assert tb.build_text() == expected_built_text
		facets = tb.build_facets()
		assert len(facets) == 1
		facet = facets[0]
		assert facet.features[0].uri == expected_uri
		# byte indexes should slice the *trimmed* uri back out of the built text
		built_bytes = tb.build_text().encode("utf-8")
		assert built_bytes[facet.index.byte_start:facet.index.byte_end].decode("utf-8") == expected_uri

	def test_balanced_parens_kept_in_url(self):
		# Wikipedia-style URLs with balanced parens should not have the ) stripped
		url = "https://en.wikipedia.org/wiki/Foo_(bar)"
		text = f"see {url} for more"
		tb = bot.build_rich_text(text)
		assert tb.build_text() == text
		facets = tb.build_facets()
		assert len(facets) == 1
		assert facets[0].features[0].uri == url
