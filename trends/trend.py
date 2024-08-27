from pytrends.request import TrendReq

class GoogleTrends:
    """Class for fetching Google Trends data."""

    def __init__(self, region='czech_republic', language='cs-CZ', timezone=360):
        self.pytrends = TrendReq(hl=language, tz=timezone)
        self.region = region

    def get_trending_searches(self):
        """Fetch the current trending searches for a specified region."""
        trending_searches_df = self.pytrends.trending_searches(pn=self.region)
        trending_searches = trending_searches_df[0].tolist()  # Convert to list
        return trending_searches
