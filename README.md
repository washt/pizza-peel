# Pizza Peel 🍕
- a site selection tool for pizza franchises

## Install and Run
`chmod +x ./venv/bin/activate`
`./venv/bin/activate`

- Create DB & Load Data


- Run server
`pip3 install -r requirements.txt`
`FLASK_APP=server flask run`

## API

Given a set of coordinates, return the top five nearest bars, along with their respective square footage.
POST /bars (lat, long)

{[
  
]}

We’re going to build an API for a late-night pizza franchise that wants help with site selection.

Specifically, they’d like a tool that allows them to input a location (latitude/longitude), and returns a list of the 5 nearest bars along with their building square footage (as a proxy for capacity). 

The core of this challenge consists of the following steps:

Prep
Load the data. In this google drive there are two relevant datasets:
OpenStreetMap features with tags amenity:bar, amenity:pub, amenity:biergarten, or amenity:winery in Washington DC (extracted from the Google BigQuery bigquery-public-datasets project)
MS Building Footprints for District of Columbia
(The google drive contains the data that’s pre-clipped and ready to load, but the dataset links are there to provide you with some more detail on their contents if needed). Please load these into a database of your choice (postgres, BigQuery, etc).
Join the data. Each of the OSM features is a point representing a bar location. The MS Building Footprints are polygons representing (approximated) building footprints in DC. Please do the geospatial operations necessary to approximate the building square footage for each bar point in the dataset. Document any assumptions you make (or any edge cases you would address as follow-on work) within the repo README.
Simple API
Next, build a simple API that takes a latitude, longitude pair as input and returns the names and locations of the 5 nearest bars to the input location, along with the approximated square footage of each bar. 
Document
Please add a repo README that contains the following:
A brief description of your process for joining the data – particularly addressing (a) any assumptions you made in estimating square footage for each bar, and (b) what edge cases exist here that you would address as follow-on work.
Instructions for the customer on how to query the API and interpret the response.

Please share a github repo containing your work (prep code, API code, and README) with us (lindsay-pettingill,, amalokin, bdejesus and petzel).

If you’re finished with the basic challenge before 3-4 hours and want to keep going, here are some options
Containerize
Containerize your Prep and API code with a Dockerfile so that it can be deployed locally or on a cloud someplace. Update your README to provide instructions to the customer on how they could deploy it in production.
Choose your own feature updates!
The core API we’ve defined is pretty basic. What improvements would you make? Maybe you could add additional input options like addresses, or incorporate additional data sources like online reviews. Feel free to add additional features that are interesting or fun for you to implement. 

We’re excited to see what you come up with!
