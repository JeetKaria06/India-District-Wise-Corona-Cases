# India-District-Wise-Corona-Cases
It will show the map of the India (even in dark mode) and shows corona case (active, cured and deaths) count, distributed district wise. One can also toggle between the active, cured and death cases with just a click.

# Technologies Used
* [Beautiful Soup - Python's Web Scraping Library](https://www.crummy.com/software/BeautifulSoup/) <br>
* [Mapbox API - Open Source Mapping Platform](https://docs.mapbox.com/api/maps/) <br>
* [Nominatim Open Steet Map API - Open Source Geocoding with OpenStreetMap Data](https://nominatim.org/release-docs/develop/api/Overview/) <br>
* [Plotly Python - Open Source Graphing Library](https://plotly.com/python/) <br>

# Workflow
* Identifying valid resource for corona cases of the India. <br>
* Gathering data from a valid source state-wise and district-wise (according to requirement) and storing it in a dataframe in python. <br>
* Generating latitudes and longitudes of the district with corona cases and saving it in a .csv file.
* Matching infected districts corona case data with the latitude and longitude previously stored in .csv file.
* Plotting it on a map with suitable labels (i.e. active, cured and deaths)

# Requirements
