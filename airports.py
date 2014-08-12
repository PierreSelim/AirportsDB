# -*- coding: utf-8  -*-
import pywikibot
import pywikibot.data.wikidataquery as pwq
import json

def item_from_id(repo, identifier):
    return pywikibot.ItemPage(repo, "Q%s" % identifier)

def fetch_property_values(item, prop):
    target = None
    if prop in item.claims:
        claim = item.claims[prop][0] 
        target = claim.getTarget()
    return target

class Airport:
    def __init__(self, iata=None, icao=None, en=None, geo=None):
        self.values = {
            'iata': iata,
            'icao': icao,
            'en': en,
            'geo': geo
            }

    def __repr__(self):
        """ string to for print. """
        vals = [self.values['iata'], self.values['icao'], self.values['en'], self.values['geo']]
        display_vals = ['' if v is None else v for v in vals]
        return u';'.join(display_vals).encode('utf-8')
        

def main():
    """ Main script of airport dabatase creation. """
    from argparse import ArgumentParser
    
    parser = ArgumentParser(description="Commons Cat Metrics")
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
        page = pywikibot.Page(site, u"Aéroport de Paris-Orly")
        item = pywikibot.ItemPage.fromPage(page)
        dictionary = item.get()

        # retrieve airport list
        q= pwq.HasClaim(31,items=[1248784])
        dat = pwq.WikidataQuery(cacheMaxAge=600).query(q)
        items = dat['items']
        print "Found %d items for query: %s\n" % (len(items), q)
        for i in items:
            item = item_from_id(repo, i)
            item.get()
            name = ''
            if 'enwiki' in item.sitelinks:
                name = item.sitelinks['enwiki']
            coordinate = fetch_property_values(item, 'P625')
            latitude = ''
            longitude= ''
            if coordinate is not None:
                latitude = coordinate.lat
                longitude = coordinate.lon
            airport = Airport(iata=fetch_property_values(item, 'P238'),
                    icao= fetch_property_values(item, 'P239'),
                    geo= "%s, %s" % (latitude, longitude),
                    en=name)
            output.write(repr(airport)+'\n')
    
if __name__ == '__main__':
    main()
