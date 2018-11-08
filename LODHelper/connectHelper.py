from SPARQLWrapper import SPARQLWrapper, JSON, N3
from rdflib import Graph

class ConnectHelper():
    def __init__(self):
        super().__init__()

    def connect(self):
        try:
            self.endpoint = SPARQLWrapper("http://dbpedia.org/sparql")
        except Exception as e:
            print(str(e))

    def concWords(self, old):
        newW = ''
        for word in old:
            newW += word
        return newW

    ###
    ##
    def send_get_query(self, sub):
        self.connect()

        ## CHECK IF SUBJECT IS MORE THAN ONE WORD
        try:
            l = sub.split(' ')
            if len(l) > 1:
                sub = self.concWords(l)
        except Exception as e:
            print(str(e))
        print(sub)

        ## MAKE CUSTOM QUERY
        query_string = (f"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
                        "SELECT ?label\n"
                        "WHERE {\n"
                        f"<http://dbpedia.org/resource/{sub}> rdfs:label ?label\n"
                        "} ORDER BY ?label LIMIT 10")
        
        ## FETCH RESULTS FROM DBPEDIA
        try:
            self.endpoint.setQuery(query_string)
            self.endpoint.setReturnFormat(JSON)
            results = self.endpoint.query().convert()

            ## VIEW RESULTS
            for result in results["results"]["bindings"]:
                print(result["label"],' ---- ', result["label"]["value"])
        except Exception as e:
            print(str(e))


    ###
    ##
    def send_ask_query(self, sub):
        self.connect()

        ## CHECK IF SUBJECT IS MORE THAN ONE WORD
        try:
            l = sub.split(' ')
            if len(l) > 1:
                sub = self.concWords(l)
        except Exception as e:
            print(str(e))
        print(sub)

        ## MAKE CUSTOM QUERY
        query_string = ("ASK WHERE {\n"
                        f"<http://dbpedia.org/resource/{sub}> rdfs:label \"{sub}\"@en\n"
                        "}")
        print(query_string)

        ## FETCH RESULTS FROM DBPEDIA
        try:
            self.endpoint.setQuery(query_string)
            self.endpoint.setReturnFormat(JSON)
            results = self.endpoint.query().convert()
            ## VIEW RESULTS
            for item in results.items():
                print(results)
        except Exception as e:
            print(str(e))

       


    ###
    ##
    def send_desc_query(self, sub):
        self.connect()

        ## CHECK IF SUBJECT IS MORE THAN ONE WORD
        try:
            l = sub.split(' ')
            if len(l) > 1:
                sub = self.concWords(l)
        except Exception as e:
            print(str(e))
        print(sub)

        ## MAKE CUSTOM QUERY
        query_string = ("PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
                        "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
                        "PREFIX skos: <http://www.w3.org/2004/02/skos/core#>\n"
                        "DESCRIBE ?x WHERE {\n"
                        f"?x rdfs:label \"{sub}\"@en\n"
                        "} LIMIT 10")
        print(query_string)
        ## FETCH DATA FROM DBPEDIA
        try:
            self.endpoint.setQuery(query_string)
            self.endpoint.setReturnFormat(N3)
            results = self.endpoint.query().convert()
            ## VIEW RESULTS
            g = Graph()
            g.parse(data=results, format="n3")
            print(g.serialize(format='n3'))
        except Exception as e:
            print(str(e))

        
