# -*- coding: utf-8  -*-

import pywikibot
import pywikibot.data.wikidataquery as pwq


def item_from_id(repo, identifier):
    """ Get item from its ID.

    Args:
        repo: data repository of the site.
        identifier (int): ID of an item (eg. 120 for Q120)
    """
    return pywikibot.ItemPage(repo, "Q%s" % identifier)


def fetch_property_values(item, prop):
    """ Fetch a property from an item. """
    target = None
    if prop in item.claims:
        claim = item.claims[prop][0]
        target = claim.getTarget()
    return target


class Airport(object):

    """ Object to represent an airport and its data. """

    def __init__(self, iata=None, icao=None, en=None, geo=None, country=None):
        """ Constructor of airport.

        Args:
            iata (str): IATA code of the Airport (P238)
            icao (str): ICAO code of the Airport (P239)
            en (str): Name of the english wikipedia article about the airport
            geo (str): lat, long of the airport.
        """
        self.values = {
            'iata': iata,
            'icao': icao,
            'en': en,
            'geo': geo,
            'country': country
        }

    def __repr__(self):
        """ string to for print. """
        vals = [self.values['iata'],
                self.values['icao'],
                self.values['en'],
                self.values['geo'],
                self.values['country']]
        display_vals = ['' if v is None else v for v in vals]
        return u';'.join(display_vals).encode('utf-8')


def main():
    """ Main script of airport dabatase creation. """
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Airport DB")
    parser.add_argument("-f", "--f",
                        type=str,
                        dest="output",
                        metavar="FILE",
                        required=True,
                        help="output file")
    args = parser.parse_args()

    with open(args.output, 'w', 0) as output:

        site = pywikibot.Site("fr", "wikipedia")
        repo = site.data_repository()

        # retrieve airport list
        query = pwq.HasClaim(31, items=[1248784])
        dat = pwq.WikidataQuery(cacheMaxAge=600).query(query)
        items = dat['items']
        print "Found %d items for query: %s\n" % (len(items), query)
        for i in items:
            item = item_from_id(repo, i)
            item.get()
            name = ''
            if 'enwiki' in item.sitelinks:
                name = item.sitelinks['enwiki']
            coordinate = fetch_property_values(item, 'P625')
            latitude = ''
            longitude = ''
            if coordinate is not None:
                latitude = coordinate.lat
                longitude = coordinate.lon
            airport = Airport(iata=fetch_property_values(item, 'P238'),
                              icao=fetch_property_values(item, 'P239'),
                              geo="%s, %s" % (latitude, longitude),
                              country=fetch_property_values(item, 'P17'),
                              en=name)
            output.write(repr(airport) + '\n')

if __name__ == '__main__':
    main()
