import requests
from bs4 import BeautifulSoup
import sys, csv, contextlib, io, getopt
import wptools
import networkx as nx
from bidi.algorithm import get_display

def parse_movie_page(page_url, file):
    html_text = requests.get(page_url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    name_tag = soup.find('span')        # Getting the movie's name (+ year)
    movie_name = name_tag.string + name_tag.next_sibling.string

    dubbers_tag = None
    for title in soup.find_all('h3'):       # Finding the dubbers list. Some movie pages don't have them,
        if (title.string == 'מדבבים'):      # So we abandon this page.
            dubbers_tag = title

    if (dubbers_tag == None):
        return
    
    curr_div = dubbers_tag.next_sibling
    num_of_dubbers = 0

    while (not curr_div.has_attr('class')):     # Counting the number of dubbers.
        num_of_dubbers += 1
        curr_div = curr_div.next_sibling
        if (curr_div == None):
            break

    data_list = [movie_name]                    # Building the row data, starting with the name,
    curr_div = dubbers_tag.next_sibling         # then adding the dubbers in the next loop.

    for x in range(num_of_dubbers):
        try:
            data_list.append(curr_div.find('a').string)     # Some of the names does not link to a page,
        except:                                             # and thus they won't appear in an <a> block, but a <span> one.
            data_list.append(curr_div.find('span').string)
        curr_div = curr_div.next_sibling

    writer = csv.writer(file)                               # Writing to the csv file.
    writer.writerow(data_list)

def order_by_dubber():
    dubbers_list = []
    file = open('parsed_data.csv', 'r', newline='')
    reader = list(csv.reader(file))
    for row in reader:                                      # This loop collect all of the unique dubbers.
        names = row[1:]
        for name in names:
            if name in dubbers_list:
                continue
            else:
                dubbers_list.append(name) 
    dubbers_list.sort()
    ordered_file = open('ordered_data.csv', 'w', newline='')
    writer = csv.writer(ordered_file)
    writer.writerow(['Name', 'WikiData', 'Number of movies', 'Movies list'])    # First row in the file is the name of each column.
    for name in dubbers_list:
        ordered_data = [name]                                                   # The loop builds a row for each dubber, starting with their name.
        movies_list = []
        page = None
        try:
            with contextlib.redirect_stderr(io.StringIO()):                     # Getting their WikiData page (if exists).
                page = wptools.page(name, lang='he', silent=True).get_parse()
        except:
            pass
        if (page != None):
            ordered_data.append(page.data['wikidata_url'])
        else:
            ordered_data.append('')
        for row in reader:                                                      # Getting all the movies they participated in.
            if name in row:
                movies_list.append(row[0])
        ordered_data.append(len(movies_list))
        ordered_data.append(movies_list)
        writer.writerow(ordered_data)                                           # Writing the data.
    file.close()

def create_graph():
    G = nx.Graph()
    file = open('parsed_data.csv', 'r', newline='')
    reader = csv.reader(file)
    for row in reader:
        names = row[1:]
        for name in names:                                  # The data is added to the graph by the edges.
            for x in names:                                 # Each edge connects between two dubbers who worked together on a movie.
                if (x == name):                             # The edge's label is the name of the movie.
                    continue
                e = (get_display(name), get_display(x), {'title': get_display(row[0])})
                if G.has_edge(*e[:2]):
                    continue
                else:
                    G.add_edge(get_display(name), get_display(x), title=get_display(row[0]))
    print("number of nodes: ", G.number_of_nodes())
    print("number of edges: ", G.number_of_edges())
    nx.write_graphml(G, "graph.graphml")                    # Writing the graphml file.
    file.close()

def main(argv):
    ordering = False
    graphing = False

    try:
      opts, args = getopt.getopt(argv,"",["order=","graph="])
    except getopt.GetoptError:
      pass
    for opt, arg in opts:
        if opt == '--order':
            ordering = True
        elif opt == '--graph':
            graphing = True

    page_url = 'https://www.ishim.co.il/g.php?g=%D7%9E%D7%93%D7%95%D7%91%D7%91+-+%D7%96%D7%A8'
    html_text = requests.get(page_url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    for title in soup.find_all('h2'):
        if (title.string == 'סרטים זרים מדובבים'):
            list_tag = title

    curr_movie = list_tag
    print("Parsing...")
    with open('parsed_data.csv', 'w', newline='') as file:
        while(curr_movie.find_next_sibling("a") != None):
            curr_movie = curr_movie.find_next_sibling("a")
            url = 'https://www.ishim.co.il/' + curr_movie.attrs['href']
            parse_movie_page(url, file)
    print("Done!")
    if ordering:
        print("Ordering data...")
        order_by_dubber()
        print("Done!")
    if graphing:
        print("Building graph (graphml file)...")
        create_graph()
        print("Done!")

if __name__ == "__main__":
    main(sys.argv[1:])