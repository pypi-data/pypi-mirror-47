# Description
This tool converts LineString and Point data in Geojson format to Polygon data.The package obtains information such as number of lanes,  width of lanes from OSM data. f there is lane and  width of lane information, it calculates the width  of road using them. If this data does not exist, it attempts to calculate the width of road using the pre-defined values.
# Usage
python3 lipo2pol.py input.geojson --output output.geojson