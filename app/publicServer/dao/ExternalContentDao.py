import feedparser
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re

class ExternalContentDao:
    def __init__(self):
        pass

    # Forecast Locations
    HOWE_SOUND = "HOWE_SOUND"
    GEORGIA_NORTH = "GEORGIA_NORTH"
    GEORGIA_SOUTH = "GEORGIA_SOUTH"

    # Marine Condition Stations
    # Land
    PAM_ROCKS = "PAM_ROCKS"
    POINT_ATKINSON = "POINT_ATKINSON"
    GIBSONS = "GIBSONS"
    SQUAMISH_AIRPORT = "SQUAMISH_AIRPORT"

    #Buoy
    ENGLISH_BAY = "ENGLISH_BAY"
    HALIBUT_BANK = "HALIBUT_BANK"

    URLS = {
        "FORECAST": "https://weather.gc.ca/rss/marine/{area}_e.xml",
        "CONDITIONS": "https://weather.gc.ca/marine/incs/weather_conditions_ajax.php?mapID=02&siteID={area}&stationID={station}&lang=e&page=cc",
        # Date format for tides is "YYYY/MM/DD"
        # pres=? 0=>graph, 1=>HTML table, 2=> text
        "TIDES": "https://tides.gc.ca/eng/station?type=0&date={date}&sid={station_id}&tz=PST&pres=2"
    }
    CONDITION_PAGES = {
        "CURRENT_CONDITIONS": "cc",
        "PAST_24H_CONDITIONS": "p24hc",
    }

    AREA_IDS = {
        #"HOWE_SOUND": {"id": "06400", "rss_id": "06400", "display_name": "Howe Sound"},
        #"GEORGIA_NORTH": {"id": "14301", "rss_id": "14300", "display_name": "Straight of Georgia N."},
        #"GEORGIA_SOUTH": {"id": "14305", "rss_id": "14300", "display_name": "Straight of Georgia S."}
        "BOWIE_SOUTH": {"id": "01505", "rss_id": "01500", "display_name": "Bowie - southern half"},
        "CENTRAL_COAST": {"id": "02300", "rss_id": "02300", "display_name": "Central Coast from McInnes Island to Pine Island"},
        "EXPLORER_NORTH": {"id": "04808", "rss_id": "04800", "display_name": "Explorer - northwestern half"},
        "EXPLORER_SOUTH": {"id": "04804", "rss_id": "04800", "display_name": "Explorer - southeastern half"},
        "HARO_STRAIGHT": {"id": "06100", "rss_id": "06100", "display_name": "Haro Strait"},
        "HECATE_STRAIGHT": {"id": "06200", "rss_id": "06200", "display_name": "Hecate Strait"},
        "HOWE_SOUND": {"id": "06400", "rss_id": "06400", "display_name": "Howe Sound"},
        "JOHNSTONE_STRAIGHT": {"id": "06800", "rss_id": "06800", "display_name": "Johnstone Strait"},
        "JUAN_DE_FUCA_CENTRAL": {"id": "07010", "rss_id": "07010", "display_name": "Juan de Fuca Strait - central strait"},
        "JUAN_DE_FUCA_EAST_ENTRANCE": {"id": "07003", "rss_id": "07000", "display_name": "Juan de Fuca Strait - east entrance"},
        "JUAN_DE_FUCA_WEST_ENTRANCE": {"id": "07007", "rss_id": "07000", "display_name": "Juan de Fuca Strait - west entrance "},
        "QUEEEN_CHARLOTTE_SOUND_EAST": {"id": "12303", "rss_id": "12300", "display_name": "Queen Charlotte Sound - eastern half "},
        "QUEEEN_CHARLOTTE_SOUND_WEST": {"id": "12307", "rss_id": "12300", "display_name": "Queen Charlotte Sound - western half "},
        "QUEEEN_CHARLOTTE_STRAIGHT": {"id": "12400", "rss_id": "12400", "display_name": "Queen Charlotte Strait "},
        "GEORGIA_NORTH": {"id": "14301", "rss_id": "14300", "display_name": "Strait of Georgia - north of Nanaimo "},
        "GEORGIA_SOUTH": {"id": "14305", "rss_id": "14300", "display_name": "Strait of Georgia - south of Nanaimo "},
        "WEST_COAST_HAIDA_GWAII": {"id": "15205", "rss_id": "15200", "display_name": "West Coast Haida Gwaii - southern half "},
        "WEST_COAST_VANCOUVER_ISLAND_NORTH": {"id": "15300", "rss_id": "15300", "display_name": "West Coast Vancouver Island North "},
        "WEST_COAST_VANCOUVER_ISLAND_SOUTH": {"id": "16200", "rss_id": "16200", "display_name": "West Coast Vancouver Island South "},
    }

    STATION_IDS = {
#        "PAM_ROCKS": {"id": "WAS", "display_name": "Pam Rocks", "area_name": "HOWE_SOUND", "type": "land"},
#        "POINT_ATKINSON": {"id": "WSB", "display_name": "Point Atkinson", "area_name": "GEORGIA_SOUTH", "type": "land"},
#        "SQUAMISH_AIRPORT": {"id": "WSK", "display_name": "Squamish Airport", "area_name": "GEORGIA_SOUTH", "type": "land"},
#        "WEST_VANCOUVER": {"id": "WWA", "display_name": "West Vancouver", "area_name": "GEORGIA_SOUTH", "type": "land"},
#        "VANCOUVER_HARBOUR": {"id": "WHC", "display_name": "Vancouver Harbour", "area_name": "GEORGIA_SOUTH", "type": "land"},
#        "VANCOUVER_INTL_AIRPORT": {"id": "YVR", "display_name": "Vancouver Int'l Airport", "area_name": "GEORGIA_SOUTH", "type": "land"},
#        "SAND_HEADS": {"id": "WVF", "display_name": "Sand Heads Lighthouse", "area_name": "GEORGIA_SOUTH", "type": "land"},
#        "TSAWWASSEN": {"id": "VTF", "display_name": "Tsawwassen Ferry Terminal", "area_name": "GEORGIA_SOUTH", "type": "land"},
#        "SATURNA_ISLAND": {"id": "WEZ", "display_name": "Saturna Island", "area_name": "GEORGIA_SOUTH", "type": "land"},


        "BALLENAS_ISLANDS": {"id": "WGB", "display_name": "Ballenas Islands", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "BELLA_BELLA_AP": {"id": "BBC", "display_name": "Bella Bella Airport", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "BELLA_COOLA_AP": {"id": "YBD", "display_name": "Bella Coola Airport", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "CAMPBELL_RIVER_AP": {"id": "YBL", "display_name": "Campbell River Airport", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "CAPE_ST_JAMES": {"id": "WZV", "display_name": "Cape St.James", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "CATHEDRAL_POINT": {"id": "WME", "display_name": "Cathedral Point", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "COMOX_AP": {"id": "YQQ", "display_name": "Comox Airport", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "DISCOVERY_ISLAND": {"id": "WDR", "display_name": "Discovery Island", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "ENTRANCE_ISLAND": {"id": "WEL", "display_name": "Entrance Island", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "ESQUIMALT_HARBOUR": {"id": "WPF", "display_name": "Esquimalt Harbour", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "ESTAVAN_POINT": {"id": "WEB", "display_name": "Estevan Point", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "FANNY_ISLAND": {"id": "XFA", "display_name": "Fanny Island", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "GRIEF_POINT": {"id": "WKA", "display_name": "Grief Point", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "HERBERT_ISLAND": {"id": "WLP", "display_name": "Herbert Island", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "PAM_ROCKS": {"id": "WAS", "display_name": "Howe Sound - Pam Rocks", "area_name": "HOWE_SOUND", "type": "land"},
        "KELP_REEFS": {"id": "WZO", "display_name": "Kelp Reefs", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "MALAHAT": {"id": "WKH", "display_name": "Malahat", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "NANAIMO_AP": {"id": "YCD", "display_name": "Nanaimo Airport", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "POINT_ATKINSON": {"id": "WSB", "display_name": "Point Atkinson", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "PORT_ALBERNI": {"id": "WQC", "display_name": "Port Alberni", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "PORT_HARDY_AP": {"id": "YZT", "display_name": "Port Hardy Airport", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "POWELL_RIVER_AP": {"id": "YPW", "display_name": "Powell River Airport", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "RACE_ROCKS_LIGHT_STN": {"id": "WQK", "display_name": "Race Rocks Lightstation", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "SAND_HEADS_LIGHT_STN": {"id": "WVF", "display_name": "Sand Heads Lightstation", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "SARTINE_ISLAND": {"id": "WFG", "display_name": "Sartine Island", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "SATURNA_ISLAND": {"id": "WEZ", "display_name": "Saturna Island", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "SECHELT": {"id": "VOU", "display_name": "Sechelt", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "SHERINGHAM_POINT": {"id": "WSP", "display_name": "Sheringham Point", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "SISTERS_ISLETS": {"id": "WGT", "display_name": "Sisters Islets", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "SOLANDER_ISLAND": {"id": "WRU", "display_name": "Solander Island", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "SQUAMISH_AP": {"id": "WSK", "display_name": "Squamish Airport", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "TOFINO_AP": {"id": "YAZ", "display_name": "Tofino Airport", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "TSAWWASSEN": {"id": "VTF", "display_name": "Tsawwassen Ferry Terminal", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "VANCOUVER_HARBOUR": {"id": "WHC", "display_name": "Vancouver Harbour", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "VANCOUVER_INTL_AP": {"id": "YVR", "display_name": "Vancouver Int'l Airport", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "VICTORIA_GONZALES": {"id": "WLM", "display_name": "Victoria Gonzales", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "VICTORIA_INTL_AP": {"id": "YYJ", "display_name": "Victoria Int'l Airport", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "VICTORIA_UNIVERSITY": {"id": "WYJ", "display_name": "Victoria, University of", "area_name": "GEORGIA_SOUTH", "type": "land"},
        "WEST_VANCOUVER": {"id": "WWA", "display_name": "West Vancouver", "area_name": "GEORGIA_SOUTH", "type": "land"},


        "ENGLISH_BAY": {"id": "46304",  "display_name": "English Bay", "area_name": "GEORGIA_SOUTH", "type": "buoy"},
        "HALIBUT_BANK": {"id": "46146", "display_name": "Halibut Bank", "area_name": "GEORGIA_SOUTH", "type": "buoy"},
        "EAST_DELLWOOD": {"id": "14305", "display_name": "East Dellwood", "area_name": "GEORGIA_SOUTH", "type": "buoy"},
        "GEORGIA_STRAIGHT": {"id": "46303", "display_name": "Georgia Strait", "area_name": "GEORGIA_SOUTH", "type": "buoy"},
        "LA_PEROUSE_BANK": {"id": "46206", "display_name": "La Perouse Bank", "area_name": "GEORGIA_SOUTH", "type": "buoy"},
        "SENTRY_SHOAL": {"id": "46131", "display_name": "Sentry Shoal", "area_name": "GEORGIA_SOUTH", "type": "buoy"},
        "SOUTH_BROOKS": {"id": "46132", "display_name": "South Brooks", "area_name": "GEORGIA_SOUTH", "type": "buoy"},
        "SOUTH_HECATE_STRAIGHT": {"id": "46185", "display_name": "South Hecate Strait", "area_name": "GEORGIA_SOUTH", "type": "buoy"},
        "SOUTH_MORESBY": {"id": "46147", "display_name": "South Moresby", "area_name": "GEORGIA_SOUTH", "type": "buoy"},
        "SOUTH_NOMAD": {"id": "46036", "display_name": "South Nomad", "area_name": "GEORGIA_SOUTH", "type": "buoy"},
    }


    TIDE_STATION_IDS = {
        "BOAT_HARBOUR": {"id": "7480", "display_name": "Boat Harbour"},
        "BOOM_ISLET": {"id": "7843", "display_name": "Boom Islet"},
        "DIONISIO_POINT": {"id": "7535", "display_name": "Dionisio Point"},
        "GIBSONS": {"id": "7820", "display_name": "Gibsons"},
        "HALFMOON_BAY": {"id": "7830", "display_name": "Halfmoon Bay"},
        "NANAIMO": {"id": "7917", "display_name": "Nanaimo"},
        "NEW_WESTMINSTER": {"id": "7654", "display_name": "New Westminster *"},
        "POINT_ATKINSON": {"id": "7795", "display_name": "Point Atkinson *"},
        "PORPOISE_BAY": {"id": "7852", "display_name": "Porpoise Bay"},
        "PORT_MOODY": {"id": "7755", "display_name": "Port Moody"},
        "SAND_HEADS": {"id": "7594", "display_name": "Sand Heads"},
        "SILVA_BAY": {"id": "7550", "display_name": "Silva Bay"},
        "SQUAMISH": {"id": "7811", "display_name": "Squamish"},
        "STEVESON": {"id": "7607", "display_name": "Steveston"},
        "TSAWWASSEN": {"id": "7590", "display_name": "Tsawwassen"},
        "VANCOUVER": {"id": "7735", "display_name": "Vancouver *"},
        "WHITE_ROCK": {"id": "7577", "display_name": "White Rock"}
    }


    TIDE_DATE_FORMAT = "%Y/%m/%d"

    def get_forecast_areas(self):
        areas = list(self.AREA_IDS.keys());
        areas.sort()
        return areas

    def get_condition_stations(self, station_type):
        if not station_type:
            stations = list(self.STATION_IDS.keys())
            stations.sort()
            return stations

        stations = []
        for key, value in self.STATION_IDS.items():
            if value["type"] == station_type:
                stations.append(key)
        stations.sort()
        return stations

    def get_tide_stations(self):
        stations = list(self.TIDE_STATION_IDS.keys())
        stations.sort()
        return stations

    def get_marine_forecast(self, location):
        site = ExternalContentDao.__get_info_for_location(location, self.AREA_IDS)
        forecast = {"location": site["display_name"], "forecastEntries": []}
        NewsFeed = feedparser.parse(self.URLS["FORECAST"].replace("{area}", site["rss_id"]))
        # print ('Number of entries'+str(len(NewsFeed.entries)))
        # print (NewsFeed)
        # print (entry.keys())
        forecast["forecastEntries"].extend(NewsFeed.entries)
        return forecast

    def get_marine_conditions(self, station_name):
        station = ExternalContentDao.__get_info_for_location(station_name, self.STATION_IDS)
        site = ExternalContentDao.__get_info_for_location(station["area_name"], self.AREA_IDS)
        conditions = {"location": site["display_name"], "station": station["display_name"], "conditionEntries": []}
        url = self.URLS["CONDITIONS"].replace("{area}", site["id"]).replace("{station}", station["id"])
        #print("Trying to open url: "+url);
        response = urllib.request.urlopen(url)
        raw_data = response.read()
        encoding = response.info().get_content_charset('utf8')
        # print(encoding)
        # print(type(response))
        conditions["conditionEntries"].extend(self.__parseConditions(raw_data.decode(encoding)))
        return conditions

    def get_tides(self, station_name, start_date):
        station = ExternalContentDao.__get_info_for_location(station_name, self.TIDE_STATION_IDS)
        tide_data = {"location": station["display_name"], "station_id": station["id"], "timezone": "PST", "tide_entries": []}
        url = self.URLS["TIDES"].replace("{station_id}", station["id"]).replace("{date}", urllib.parse.quote(start_date.strftime(self.TIDE_DATE_FORMAT)))
        # print("Getting url: "+url)
        response = urllib.request.urlopen(url)
        raw_data = response.read()
        encoding = response.info().get_content_charset('utf8')
        tide_data["tide_entries"] = ExternalContentDao.__parse_tides(raw_data.decode(encoding))
        return tide_data

    @staticmethod
    def __get_info_for_location(location, location_list):
        if location not in location_list:
            raise ValueError("Invalid location " + location)
        site = location_list[location]
        if not site:
            raise ValueError("Invalid location "+location)
        return site

    def __parseConditions(self, html_conditions):
        data = []
        soup = BeautifulSoup(html_conditions, "html.parser")
        if soup.find("table") and soup.find("table").find("tbody"):
            for row in soup.find("table").find("tbody").find_all("tr"):
                key = row.find("th");
                while key:
                    value = key.find_next_sibling("td")
                    data.append({"title": key.renderContents().decode().replace("\xa0"," "), "value": value.text})
                    key = value.find_next_sibling("th")
                #data.append(row)
        else:
            data.append({"title": "Error", "value": "No data available"})
        return data

    @staticmethod
    def __parse_tides(html_tides):
        data = []
#        print("Trying to parse "+html_tides)
        soup = BeautifulSoup(html_tides, "html.parser")

        tide_lines = soup.find("div", "stationTextData").find_all("div")

        # print(tide_lines)
        for tide_line in tide_lines:
            text = tide_line.renderContents().decode()
            parts = text.strip().split(";")
            if len(parts) == 4:
                tide_entry = {"time": parts[0].strip()+"T"+parts[1], "height_m": re.sub(r"\(.*$", "", parts[2]), "height_ft": re.sub(r"\(.*$", "", parts[3].strip())}
                data.append(tide_entry)
            else:
                print("Unknown tide data format "+tide_line)
        # print(data)
        return data

#Conditions: https://weather.gc.ca/marine/incs/weather_conditions_ajax.php?mapID=02&siteID=06400&stationID=WAS&lang=e&page=cc
# Pages: cc = current conditions
#        p24hc = previous 24h conditions
#    var page = function(){
#    if(href()[0].indexOf('currentConditions') !== -1){
#    return 'cc';
#    }else if(href()[0].indexOf('24hrObsHistory') !== -1){
#    return 'p24hc';
#}else if(href()[0].indexOf('regionalSummary') !== -1){
#return 'rs';
#}else if(href()[0].indexOf('lightstation') !== -1){
#return 'ls';
#}
#
#return false;
#};
#
#// sends an ajax request to weather_conditions_ajax.php
#                            // on success, clear the weather conditions tab and load the returned html
#$.ajax({
#    type: 'GET',
#    cache: false,
#    url: '/marine/incs/weather_conditions_ajax.php?' + href()[1] + '&lang=' + lang + '&page=' + page(),
#}).done(function(html){
#    contentContainer.empty();
#contentContainer.append(html);
#
#$('html, body').animate({ scrollTop : $('#weather-conditions-lnk').offset().top }, 'slow');
#
#var baseWidth = 590, \
#                baseCoords = [];
#
#$('img[usemap]').each(function(){
#    var thisImg = $(this), \
#                   currentWidth = thisImg.width(), \
#                                  offset = parseFloat((currentWidth / baseWidth).toFixed(4));
#
#$(thisImg.attr('usemap')).children().each(function(i){
#    var thisArea = $(this);
#
#var coords = thisArea.attr('coords').split(',');
#
#baseCoords[i] = [
#    coords[0],
#    coords[1],
#    coords[2],
#];
#
#var x = Math.round(parseInt(baseCoords[i][0]) * offset), \
#        y = Math.round(parseInt(baseCoords[i][1]) * offset);
#
#thisArea.attr('coords', x + ',' + y + ',' + baseCoords[i][2]);
#});
#});
#});