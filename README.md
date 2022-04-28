# Pizza Peel 🍕
- a tool to help pizza restaurateur's keep their eyes peeled 👀 for potential new locations.

## Install and Run
`chmod +x venv/bin/activate`
`./venv/bin/activate`
`pip3 install -r requirements.txt`

- Run server
`FLASK_APP=server flask run`

## API

Given a set of coordinates, return the top five nearest bars, along with their respective area.

### Request
POST /nearest_bars { "lat":  "-77.0380051", "long": "38.9039033" } 

```
curl --location --request POST 'localhost:5001/nearest_bars/' \
--header 'Content-Type: application/json' \
--data-raw '{ "lat":  "-77.0380051", "long": "38.9039033"}'
```

### Response
results will be returned as a JSON array with each entry containing an array of `name`, `coordinates`, and `site area` in meters squared
{[
    [
        "Barcode",
        [
            -77.0380051,
            38.9039033
        ],
        26616.163640099174
    ],
    [
        "Off The Record",
        [
            -77.038828,
            38.9028416
        ],
        10051.345871848793
    ],
    [
        "Bravo Bravo",
        [
            -77.0392331,
            38.9029189
        ],
        10051.345871848793
    ],
    [
        "Archibald's/Fast Eddies Billiards Cafe",
        [
            -77.035585,
            38.9021339
        ],
        1579.3149046856142
    ],
    [
        "The Bottom Line",
        [
            -77.0401739,
            38.9009945
        ],
        23084.5228926401
    ]
]}

## Data Joining Process 
My joining algo can be seen in `preprocess.py`, which was used to create `data/joined_data.json` for the main application. I had some trouble initially loading in the `osm-bars` data because I've never worked with `.shp` files before..this set me back ~1 hour.

I brute forced a solution to match location points with their respective footprint data by using `shapely.Polygon.within`, then calulating the area.

There are definitely some optimizations available here..however my thinking was since building footprints shouldn't change very often and given the time limit of the exercise a brute force approach would be okay for now. `preprocess.py` took about 5 minutes to run on my 2020 Macbook Pro. If the input data were widened to the entire country, I'd probably use a balanced tree to reduce the search time in the joining process.

I don't think the projection calculation is correct based on the numbers I'm seeing in the result (way too big!!). Given the time constraint I had to abandon investingating why but I have a hunch that I may be using the wrong geodetic transform value. Additionally, the footprint calculation assumes a 1:1 with building size, which isn't very accuate (floor plan layout, dead space, multitple floors, etc..) I'd pull in MLS or zoning data to get a more accurate square footage number.

## Server Process
I use `scipy`s `KDTree` to store and find nearest bars for a given latitude and longitude.

## If I had more time,,,

I would add some more documentation + unit tests for the transform functionm, KDTree lookup and some e2e tests for api request/response.

I'd add a persistant data layer and define schema for the bar location data. Although to be honest, I'm not sure how to find the closest neighbors efficiently with a SQL query...I'd probably take an hour or two more of research. 

I also had some issues with my local python enviornment, so I might add containerization to make dev setup easier.