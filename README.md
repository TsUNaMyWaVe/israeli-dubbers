# Israeli Dubbers Collection as Data
A university project for the Digital Humanities course in Ben Gurion University, by Lia Rubinstein.

## Intial Data Description
The data intially came from the website ["Ishim"](https://www.ishim.co.il/), which is a vast database about the Israeli media creations. As such, it also contains the data about dubbed movies, and who dubbed in them. The details about the data you can find there however, are pretty scarce. Each actor page conatins very little data, and the way the site is built prevents us from arriving at any meaningful conclusions of the data in it.

## Current Data Description
My final data is available here in 2 differen type of files: a csv file, and an OpenRefine project. Each entry in the table represents a dubber. Every entry includes the following data:
* Number of movies the actor dubbed in
* A list of those movies, and the year the (dubbed) movie was released

Aside from those (which were gathered directly from "Ishim" site), using OpenRefine and WikiData, some of the entries have additional data:
* Additional occupations
* Date of birth
* Place of birth
* Sex or gender

Using all this files we can now use the data in a more convenient way, and reach conclusions based on what we are looking for.
For example, we can see in what years more movies where dubbed; how many male actors are there with a big list of movies in comparison to female ones; and so on.
In addition, the OpenRefine project file also includes a reconciled version of the movies, for further use.

## Code
The code was written in Python, and is mostly used for the intiail data collection from "Ishim".
The code parse the HTML in "Ishim" to make a csv file named "parsed_date", where each entry is a movie and the list of the dubbers who participated in it.
To run it, simply perform:
```python html_parse.py```

### Required Libraries
Main dependencies:
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Requests](https://requests.readthedocs.io/en/master/)

Dependencies for extra featurs:
* [wptools](https://github.com/siznax/wptools)
* [NetworkX](https://networkx.org/)
* [Python BiDi](https://github.com/MeirKriheli/python-bidi)

### Extra Features
#### Order
Will make another csv file named "ordered_data", where each entry is a dubber with the following data:
* Number of movies they participated in
* A list of those movies
* A URL to their WikiData page (if exists)

To run it, simply perform:
```python html_parse.py order=="true"```

**Note:** Performing this step of the code will make the process significally slower, because it is accessing the WikiData API.

#### Graph
Initially I planned to display the data I collected as some kind of graph. While personally I didn't end up using it, I decided to keep the code of it for anyone who might find it useful.
Allowing this step will crate a graphml file named "graph", which will includ the data of a multi-graph, where every node is a dubber. Each edge in the graph connects two dubbers who worked together on a movie, and the edge label is the name of said movie.

To run it, simply perform:
```python html_parse.py graph=="true"```

**Note:** Most of the common graphing applications can open and manipulate graphml files. But please understand that the code as-is is using the entire parsed database to make the graph, and so it's a very big graph. When opening this file in such application, it might not be easy to read/manipulate, depending on the application you use and your computer performance.

## Display
The way I decided to display the data is to contribute to WikiData. Out of the 1478 dubbers entries I worked with, only about ~34% had a WikiData page. Thus OpenRefine was used once again, to push the following changes into WikiData:
* Creating a WikiData page for each dubber who didn't already have one
* Adding the occupation "dub actor" to every new page and to every existing page that didn't have any occupation listed before

It ended up being more than 1200 edits, which are reflected in [my contribuation page in WikiData](https://www.wikidata.org/w/index.php?title=Special:Contributions/TsUNaMy_WaVe).

## In Conclusion
Starting from a website which is an archive for humans, the dubbers data changed and evolved to a proper dataset. But the dubbing industry does not stop, and so the tools and methods described here can be used to update the collection as needed.
