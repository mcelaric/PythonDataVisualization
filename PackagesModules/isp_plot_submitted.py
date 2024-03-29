"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    with open(filename, 'r') as csvfile:
        rows_as_dicts = {}
        reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        # Make each CSV row a dictionary
        # Then add these row dicts to the 'outer' dict by keyfield in each row
        for row in reader:
            temp = dict(row)
            rows_as_dicts[temp.get(keyfield)] = temp
            
    return rows_as_dicts


def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    plot_vals = []
    print("gdpdata.keys - ", gdpdata.keys())
    print("gdpdata - ", gdpdata)
    for year in range(gdpinfo.get("min_year"), gdpinfo.get("max_year")+1):
        if str(year) in gdpdata.keys():
            #print("gpd data - ", gdpdata.get(str(year)))
            # Sneaky!!!  Not all years have data!
            # Can't plot data that doesn't exist
            # lazy way - it works, but not very python
            # And it passes the unit tests
            #if gdpdata.get(str(year)) != '':
            #   plot_vals.append((year, float(gdpdata.get(str(year)))))
            # Handle it this way!!!
            try:
                plot_vals.append((year, float(gdpdata.get(str(year)))))
            except ValueError:
                continue
    return plot_vals

def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    plotting_data = {}
    
    for country in country_list:
        plot_points = []
        
        countries = read_csv_as_nested_dict(gdpinfo.get("gdpfile"), gdpinfo.get("country_name"), 
                                            gdpinfo.get("separator"), gdpinfo.get("quote"))
        for year in range(gdpinfo.get("min_year"), gdpinfo.get("max_year")+1):
            try:
                #print(year, countries.get(country).get(str(year)))
                plot_points.append((int(year), float(countries.get(country).get(str(year)))))
            # See comments in build_plot_values
            # but received (Exception: AttributeError) "'NoneType' 
            except (ValueError, AttributeError):
                continue

        plotting_data[country] = plot_points
        
    return plotting_data


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """

    xy_chart = pygal.XY()
    xy_chart.title = 'GDP ' + str(gdpinfo.get("min_year")) + ' - ' + str(gdpinfo.get("max_year"))
    xy_chart.y_title = 'GDP in USD ($)'
 
    for country in country_list:
        xy_chart.add(country, build_plot_dict(gdpinfo, country_list).get(country))
 
    xy_chart.render_to_file(plot_file)


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")


# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

#test_render_xy_plot()