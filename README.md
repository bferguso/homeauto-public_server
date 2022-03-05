# marine_weather
Site that scrapes and consolidates the Canadian Government marine weather website data including
regional forecasts, station conditions and tide forecasts.

The data is taken from the official Weather Canada sites.

This site is currently hosted at `https://apps.qedsystems.ca/weather`
### Webesite URLS
The following URLS are available:

- `https://<server name>/weather` : Default locations for Bowen Island including conditions at
Pam Rocks, Point Atkinson & Halibut Bank, forecasts for Howe Sound & Straight of Georgia, and Tides
for Gibsons and Point Atkinson.
- `https://<server name>/weather/custom`: Site to build an URL for a custom set of stations

### JSON endpoints
The following endpoints that return JSON data are also available:
- Available forecast locations: `https://<server name>/weather/getForecastAreas`
- Available condition locations: `https://<server name>/weather/getConditionStations`
- Available tide locations: `https://<server name>/weather/getTideStations`

The following endpoints get the conditions for the stations above:
- Marine forecast: `https://<server name>/weather/getMarineForecast?area=<area name>`
- Marine conditions: `https://<server name>/weather/getMarineConditions?station=<station name>`
- Tide information: `https://<server name>/weather/getTides?location_name=<tide station>`

