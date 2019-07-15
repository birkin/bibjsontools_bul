# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json, logging, pprint, sys, unittest
try:
    import bibjsontools  # accessed when running `python ./test.py`
except:
    sys.path.append( '../' )  # accessed when running, eg, `python ./openurl.py TestFromOpenURL.test_unicode_dump`
    import bibjsontools
from bibjsontools import from_dict
from bibjsontools import from_openurl
from bibjsontools import OpenURLParser
from bibjsontools import to_openurl
try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs


logging.basicConfig(
    level=logging.WARNING,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger('bibjsontools')


class TestFromOpenURL(unittest.TestCase):

    def test_book_from_worldcat(self):
        q = 'rft.pub=W+H+Freeman+%26+Co&rft.btitle=Introduction+to+Genetic+Analysis.&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&isbn=9781429233231&req_dat=%3Csessionid%3E0%3C%2Fsessionid%3E&title=Introduction+to+Genetic+Analysis.&pid=%3Caccession+number%3E277200522%3C%2Faccession+number%3E%3Cfssessid%3E0%3C%2Ffssessid%3E&rft.date=2008&genre=book&rft_id=urn%3AISBN%3A9781429233231&openurl=sid&rfe_dat=%3Caccessionnumber%3E277200522%3C%2Faccessionnumber%3E&rft.isbn=9781429233231&url_ver=Z39.88-2004&date=2008&rfr_id=info%3Asid%2Ffirstsearch.oclc.org%3AWorldCat&id=doi%3A&rft.genre=book'
        bib = from_openurl(q)
        self.assertEqual(bib['type'], 'book')
        self.assertEqual(bib['title'],
                        'Introduction to Genetic Analysis.')
        self.assertEqual(bib['year'], '2008')
        self.assertTrue({'type': 'oclc',
                          'id': '277200522'} in bib['identifier'])

    def test_article(self):
        q = 'volume=16&genre=article&spage=538&sid=EBSCO:aph&title=Current+Pharmaceutical+Design&date=20100211&issue=5&issn=13816128&pid=&atitle=Targeting+%ce%b17+Nicotinic+Acetylcholine+Receptors+in+the+Treatment+of+Schizophrenia.'
        bib = from_openurl(q)
        self.assertEqual(bib['journal']['name'],
                         'Current Pharmaceutical Design')
        self.assertEqual(bib['year'],
                         '2010')
        self.assertTrue({'type': 'issn',
                         'id': '13816128'} in bib['identifier'])

    def test_article_stitle(self):
        q = 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/www.isinet.com:WoK:UA&rft.spage=30&rft.issue=1&rft.epage=42&rft.title=INTEGRATIVE%20BIOLOGY&rft.aulast=Castillo&url_ctx_fmt=info:ofi/fmt:kev:mtx:ctx&rft.date=2009&rft.volume=1&url_ver=Z39.88-2004&rft.stitle=INTEGR%20BIOL&rft.atitle=Manipulation%20of%20biological%20samples%20using%20micro%20and%20nano%20techniques&rft.au=Svendsen%2C%20W&rft_id=info:doi/10%2E1039%2Fb814549k&rft.auinit=J&rft.issn=1757-9694&rft.genre=article'
        bib = from_openurl(q)
        self.assertEqual(bib['title'],
                         'Manipulation of biological samples using micro and nano techniques')
        self.assertEqual(bib['journal']['shortcode'],
                         'INTEGR BIOL')

    def test_article_full_name(self):
        q = 'issn=1040676X&aulast=Wallace&title=Chronicle%20of%20Philanthropy&pid=<metalib_doc_number>000117190</metalib_doc_number><metalib_base_url>http://sfx.brown.edu:8331</metalib_base_url><opid></opid>&sid=metalib:EBSCO_APH&__service_type=&volume=17&genre=&sici=&epage=23&atitle=Where%20Should%20the%20Money%20Go%3F&date=2005&isbn=&spage=9&issue=24&id=doi:&auinit=&aufirst=%20Nicole'
        bib = from_openurl(q)
        self.assertEqual(bib['author'][0]['name'], 'Wallace, Nicole')

    def test_bad_title(self):
        #This open url has a book title and a journal title.
        #Parser seems to handle these ok - should do some type of override to handle logical inconsistencies
        q = 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/www.isinet.com:WoK:UA&rft.spage=488&rft.issue=11-1&rft.epage=490&rft.title=JOURNAL%20OF%20THE%20AMERICAN%20CERAMIC%20SOCIETY&rft.aulast=DOLE&url_ctx_fmt=info:ofi/fmt:kev:mtx:ctx&rft.date=1977&rft.volume=60&rft.btitle=JOURNAL%20OF%20THE%20AMERICAN%20CERAMIC%20SOCIETY&url_ver=Z39.88-2004&rft.atitle=ELASTIC%20PROPERTIES%20OF%20MONOCLINIC%20HAFNIUM%20OXIDE%20AT%20ROOM-TEMPERATURE&rft.au=WOOGE%2C%20C&rft.auinit=S&rft.issn=0002-7820&rft.genre=article'
        bib = from_openurl(q)
        self.assertEqual(bib['title'], 'ELASTIC PROPERTIES OF MONOCLINIC HAFNIUM OXIDE AT ROOM-TEMPERATURE')
        #pprint(bib)

    def test_to_openurl_article(self):
        q = 'issn=1175-5652&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&rfr_id=info%3Asid%2Ffirstsearch.oclc.org%3AMEDLINE&req_dat=<sessionid>0<%2Fsessionid>&pid=<accession+number>678061209<%2Faccession+number><fssessid>0<%2Ffssessid>&rft.date=2010&volume=8&date=2010&rft.volume=8&rfe_dat=<accessionnumber>678061209<%2Faccessionnumber>&url_ver=Z39.88-2004&atitle=The+missing+technology%3A+an+international+comparison+of+human+capital+investment+in+healthcare.&genre=article&epage=71&spage=361&id=doi%3A&rft.spage=361&rft.sici=1175-5652%282010%298%3A6<361%3ATMTAIC>2.0.TX%3B2-O&aulast=Frogner&rft.issue=6&rft.epage=71&rft.jtitle=Applied+health+economics+and+health+policy&rft.aulast=Frogner&title=Applied+health+economics+and+health+policy&rft.aufirst=BK&rft_id=urn%3AISSN%3A1175-5652&sici=1175-5652%282010%298%3A6<361%3ATMTAIC>2.0.TX%3B2-O&sid=FirstSearch%3AMEDLINE&rft.atitle=The+missing+technology%3A+an+international+comparison+of+human+capital+investment+in+healthcare.&issue=6&rft.issn=1175-5652&rft.genre=article&aufirst=BK'
        bib = from_openurl(q)
        #Round trip the query
        ourl = to_openurl(bib)
        bib2 = from_openurl(ourl)
        self.assertEqual(bib['type'],
                         bib2['type'])
        self.assertEqual(bib['title'],
                          bib2['title'])
        self.assertEqual(bib['journal']['name'],
                         bib2['journal']['name'])
        self.assertEqual(bib['year'],
                         bib2['year'])

    def test_to_openurl_pmid(self):
        #Round trip the query
        q = 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/pss.sagepub.com&rft.spage=569&rft.issue=4&rft.epage=582&rft.aulast=Nolen-Hoeksema&ctx_tim=2010-11-27T19:38:39.6-08:00&url_ctx_fmt=info:ofi/fmt:kev:mtx:ctx&rft.volume=100&url_ver=Z39.88-2004&rft.stitle=J%20Abnorm%20Psychol&rft.auinit1=S.&rft.atitle=Responses%20to%20depression%20and%20their%20effects%20on%20the%20duration%20of%20depressive%20episodes.&ctx_ver=Z39.88-2004&rft_id=info:pmid/1757671&rft.jtitle=Journal%20of%20abnormal%20psychology&rft.genre=article'
        bib = from_openurl(q)
        #pprint(bib)
        ourl = to_openurl(bib)
        bib2 = from_openurl(ourl)
        #pprint(bib2)
        self.assertEqual(bib['journal']['shortcode'],
                         bib2['journal']['shortcode'])

    def from_openurl(self):
        q = 'rfr_id=info%3Asid%2Fmendeley.com%2Fmendeley&url_ctx_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Actx&rft.pages=130-146&rft.genre=bookitem&rft.aulast=Hochschild&ctx_ver=Z39.88-2004&rft.atitle=Global+Care+Chains+and+Emotional+Surplus+Value&url_ver=Z39.88-2004&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&rft.aufirst=Arlie+Russell&rft.au=Hutton%2C+Will&btitle=Your Edited Edition'
        q = 'openurl=tions.com/?sid=info:sid/sersol:RefinerQuery&genre=bookitem&isbn=9780313358647&&title=The+handbook+of+near-death+experiences+%3A+thirty+years+of+investigation&atitle=Census+of+non-Western+near-death+experiences+to+2005%3A+Observations+and+critical+reflections.&volume=&part=&issue=&date=2009-01-01&spage=135&epage=158&aulast=Kellehear%2C+Allan&aufirst= '
        bib = from_openurl(q)
        pprint(bib)

    def test_book_type(self):
        q = 'rft.pub=W+H+Freeman+%26+Co&rft.btitle=Introduction+to+Genetic+Analysis.&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&isbn=9781429233231&req_dat=%3Csessionid%3E0%3C%2Fsessionid%3E&title=Introduction+to+Genetic+Analysis.&pid=%3Caccession+number%3E277200522%3C%2Faccession+number%3E%3Cfssessid%3E0%3C%2Ffssessid%3E&rft.date=2008&genre=book&rft_id=urn%3AISBN%3A9781429233231&openurl=sid&rfe_dat=%3Caccessionnumber%3E277200522%3C%2Faccessionnumber%3E&rft.isbn=9781429233231&url_ver=Z39.88-2004&date=2008&rfr_id=info%3Asid%2Ffirstsearch.oclc.org%3AWorldCat&id=doi%3A&rft.genre=book'
        d = OpenURLParser(q)
        self.assertEqual(d.type, 'book')

    def test_article_type(self):
        q = 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/pss.sagepub.com&rft.spage=569&rft.issue=4&rft.epage=582&rft.aulast=Nolen-Hoeksema&ctx_tim=2010-11-27T19:38:39.6-08:00&url_ctx_fmt=info:ofi/fmt:kev:mtx:ctx&rft.volume=100&url_ver=Z39.88-2004&rft.stitle=J%20Abnorm%20Psychol&rft.auinit1=S.&rft.atitle=Responses%20to%20depression%20and%20their%20effects%20on%20the%20duration%20of%20depressive%20episodes.&ctx_ver=Z39.88-2004&rft_id=info:pmid/1757671&rft.jtitle=Journal%20of%20abnormal%20psychology&rft.genre=article'
        d = OpenURLParser(q)
        self.assertEqual(d.type, 'article')

    def test_bookitem_type(self):
        q = 'openurl=tions.com/?sid=info:sid/sersol:RefinerQuery&genre=bookitem&isbn=9780313358647&&title=The+handbook+of+near-death+experiences+%3A+thirty+years+of+investigation&atitle=Census+of+non-Western+near-death+experiences+to+2005%3A+Observations+and+critical+reflections.&volume=&part=&issue=&date=2009-01-01&spage=135&epage=158&aulast=Kellehear%2C+Allan&aufirst='
        d = OpenURLParser(q)
        self.assertEqual(d.type, 'inbook')

    def test_symbols_in_title(self):
        q = u"rft.title=Elective delivery at 34⁰(/)⁷ to 36⁶(/)⁷ weeks' gestation and its impact on neonatal outcomes in women with stable mild gestational hypertension&pmid=20934682&genre=journal"
        #Just round trip to see if we raise encoding errors.
        bib = from_openurl(q)
        openurl = to_openurl(bib)
        bib2 = from_openurl(openurl)

    def test_ugly_genre(self):
        q = u"genre=book\\"
        bib = from_openurl(q)
        self.assertEqual(bib['type'], 'book')
        q = "genre=articleStuff"
        bib = from_openurl(q)
        self.assertEqual(bib['type'], 'article')

    def test_unicode_dump(self):
        """
        Make sure we can dump unicode as JSON.
        """
        q = 'sid=FirstSearch:WorldCat&genre=book&isbn=9783835302334&title=Das "Orakel der Deisten" : Shaftesbury und die deutsche Aufklärung&date=2008&aulast=Dehrmann&aufirst=Mark-Georg&id=doi:&pid=<accession number>228805805</accession number><fssessid>0</fssessid>&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&req_dat=<sessionid>0</sessionid>&rfe_dat=<accessionnumber>228805805</accessionnumber>&rft_id=info:oclcnum/228805805&rft_id=urn:ISBN:9783835302334&rft.aulast=Dehrmann&rft.aufirst=Mark-Georg&rft.btitle=Das "Orakel der Deisten" : Shaftesbury und die deutsche Aufklärung&rft.date=2008&rft.isbn=9783835302334&rft.place=Göttingen&rft.pub=Wallstein&rft.genre=book&rfe_dat=<dissnote>Thesis (doctoral)--Freie Universität, Berlin, 2006.</dissnote>'
        bib = from_openurl(q)
        b = json.dumps(bib)
        nbib = json.loads(b)
        self.assertEqual(bib['title'], 'Das "Orakel der Deisten" : Shaftesbury und die deutsche Aufkla\u0308rung' )
        self.assertEqual(nbib['title'], 'Das "Orakel der Deisten" : Shaftesbury und die deutsche Aufkla\u0308rung' )
        #another
        q = 'sid=FirstSearch:WorldCat&genre=book&title=Staré písemné památky žen a dcer českých.&date=1869&aulast=Dvorský&aufirst=František&id=doi:&pid=<accession number>25990799</accession number><fssessid>0</fssessid>&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&req_dat=<sessionid>0</sessionid>&rfe_dat=<accessionnumber>25990799</accessionnumber>&rft_id=info:oclcnum/25990799&rft.aulast=Dvorský&rft.aufirst=František&rft.btitle=Staré písemné památky žen a dcer českých.&rft.date=1869&rft.place=V Praze&rft.pub=V komisi F. Rivnače&rft.genre=book&checksum=5bf4eb1a523452dc7d25171146c4ebaa&title=Brown University&linktype=openurl&detail=RBN'
        bib = from_openurl(q)
        b = json.dumps(bib)
        nbib = json.loads(b)
        self.assertEqual(bib['title'], 'Staré písemné památky žen a dcer českých.')
        self.assertEqual(nbib['title'], 'Staré písemné památky žen a dcer českých.')

    def test_unicode_in_unicode_string(self):
        """ Checks unicode querystring containing good unicode.
            Django prep example...
            >>> from django.utils.encoding import uri_to_iri  # <https://docs.djangoproject.com/en/1.9/ref/unicode/#uri-and-iri-handling>
            >>> utf8_str = request.META['QUERY_STRING']  # includes, for the example below, `aufirst=T%C5%8Dichi`
            >>> unicode_str = uri_to_iri( utf8_str )  # includes, for the example below, `aufirst=T\u014dichi`
            >>> bib_dct = from_openurl( unicode_str )
            """
        q = 'sid=FirstSearch:WorldCat&genre=book&title=Zen&date=1978&aulast=Yoshioka&aufirst=T\u014dichi&id=doi:&pid=6104671<fssessid>0</fssessid><edition>1st+ed.</edition>&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&rft.genre=book&req_dat=<sessionid>0</sessionid>&rfe_dat=<accessionnumber>6104671</accessionnumber>&rft_id=info:oclcnum/6104671&rft.aulast=Yoshioka&rft.aufirst=T\u014dichi&rft.btitle=Zen&rft.date=1978&rft.place=Osaka++Japan&rft.pub=Hoikusha&rft.edition=1st+ed.&rft.genre=book'
        self.assertEqual( str, type(q) )
        bib_dct = from_openurl( q )
        bib_json = json.dumps( bib_dct )
        bib2_dct = json.loads( bib_json )
        self.assertEqual( 'T\u014dichi', bib_dct['author'][0]['firstname'] )
        self.assertEqual( 'T\u014dichi', bib2_dct['author'][0]['firstname'] )

    def test_unicode_in_byte_string(self):
        """ Checks handling bytestring querystring containing unicode.
            Checks that handling will not fail, though it may not return ideal data if the uri was not first converted to an iri. """
        q = 'sid=FirstSearch:WorldCat&genre=book&title=Zen&date=1978&aulast=Yoshioka&aufirst=T\u014dichi&id=doi:&pid=6104671<fssessid>0</fssessid><edition>1st+ed.</edition>&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&rft.genre=book&req_dat=<sessionid>0</sessionid>&rfe_dat=<accessionnumber>6104671</accessionnumber>&rft_id=info:oclcnum/6104671&rft.aulast=Yoshioka&rft.aufirst=T\u014dichi&rft.btitle=Zen&rft.date=1978&rft.place=Osaka++Japan&rft.pub=Hoikusha&rft.edition=1st+ed.&rft.genre=book'
        q8 = q.encode( 'utf-8' )
        self.assertEqual( bytes, type(q8) )
        bib_dct = from_openurl( q8)
        bib_json = json.dumps( bib_dct )
        bib2_dct = json.loads( bib_json )
        self.assertEqual( 'T\u014dichi', bib_dct['author'][0]['firstname'] )
        self.assertEqual( 'T\u014dichi', bib2_dct['author'][0]['firstname'] )

    def test_oclc(self):
        q = 'id=info:sid/Brown-Vufind&title=Reassembling the social : an introduction to actor-network-theory /&date=2005&genre=book&pub=Oxford University Press,&edition=&isbn=0199256047&rfe_dat=<accessionnumber>58054359</accessionnumber'
        b = from_openurl(q)
        ids = b.get('identifier')
        self.assertTrue({'type': 'oclc', 'id': '58054359'} in ids)

    def test_referrer(self):
        q = 'id=info%3Asid%2FBrown-Vufind&title=Decolonization+%3A+perspectives+from+now+and+then+%2F&date=2004&genre=book&pub=Routledge%2C&edition=&isbn=0415248418&rfe_dat=%3Caccessionnumber%3E52458908%3C%2Faccessionnumber%3E'
        b = from_openurl(q)
        self.assertTrue(b['_rfr'],
                        'info:sid/Brown-Vufind')

    def test_unknown(self):
        q = 'sid=FirstSearch:WorldCat&isbn=9781118257203&title=A companion to the anthropology of Europe&date=2012&aulast=Kockel&aufirst=Ullrich&id=doi:&pid=<accession number>784124222</accession number><fssessid>0</fssessid>&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&req_dat=<sessionid>0</sessionid>&rfe_dat=<accessionnumber>784124222</accessionnumber>&rft_id=info:oclcnum/784124222&rft_id=urn:ISBN:9781118257203&rft.aulast=Kockel&rft.aufirst=Ullrich&rft.title=A companion to the anthropology of Europe&rft.date=2012&rft.isbn=9781118257203&rft.place=Chichester, West Sussex, UK ;;Malden, MA :&rft.pub=Wiley-Blackwell,&rft.genre=unknown'
        b = from_openurl(q)
        self.assertEqual(b['type'], 'book')

    def test_summon_article_type(self):
        #Summon style openurls
        q = 'ctx_ver=Z39.88-2004&amp;ctx_enc=info:ofi/enc:UTF-8&amp;rfr_id=info:sid/summon.serialssolutions.com&amp;rft_val_fmt=info:ofi/fmt:kev:mtx:journal&amp;rft.genre=news&amp;rft.atitle=The easy way to brighten your borders&amp;rft.jtitle=The Times&amp;rft.au=Joe Swift&amp;rft.date=2012-02-18&amp;rft.pub=NI Syndication Limited&amp;rft.issn=0140-0460&amp;rft.spage=14&amp;rft.externalDBID=n/a&amp;rft.externalDocID=280383175'
        b = from_openurl(q)
        self.assertEqual(b['type'], 'article')

    def test_book_chapter(self):
        q = 'genre=bookitem&isbn=9780470096222&title=Handbook+of+counseling+psychology+(4th+ed.).&volume=&issue=&date=20080101&atitle=The+importance+of+treatment+and+the+science+of+common+factors+in+psychotherapy.&spage=249&pages=249-266&sid=EBSCO:PsycINFO&aulast=Imel%2c+Zac+E.'
        b = from_openurl(q)
        self.assertEqual(b['type'], 'inbook')

        q = 'sid=info:sid/sersol:RefinerQuery&genre=bookitem&isbn=9781402032899&&title=The+roots+of+educational+change&atitle=Finding+Keys+to+School+Change%3A+A+40-Year+Odyssey&volume=&part=&issue=&date=2005&spage=25&epage=57&aulast=Miles&aufirst=Matthew'
        b = from_openurl(q)
        self.assertEqual(b['type'], 'inbook')
        #Real request that was being returned as a book - 9/13/12
        q = 'url_ver=Z39.88-2004&rft_val_fmt=info:ofi/fmt:kev:mtx:book&rft.genre=bookitem&rft.btitle=The Corsini Encyclopedia of Psychology&rft.atitle=Minnesota Multiphasic Personality Inventory&rft.date=2010-01-30&rfr_id=info:sid/wiley.com:OnlineLibrary'
        b = from_openurl(q)
        op = OpenURLParser(q)
        genre = op._find_key(['rft.genre', 'genre'])
        format = op._find_key(['rft_val_fmt'])
        #Check that the OpenURL pairs are parsed properly
        self.assertEqual(genre, 'bookitem')
        self.assertTrue(format.rindex('book') > 0)
        #Now look at the bibj itself.
        self.assertEqual(b['type'], 'inbook')
        self.assertEqual(b['title'], 'Minnesota Multiphasic Personality Inventory')
        self.assertEqual(b['journal']['name'], 'The Corsini Encyclopedia of Psychology')

    def test_multiple_isbn(self):
        q = 'rft.pub=Univ+Of+Mass+Press&rft_val_fmt=info%3Aofi/fmt%3Akev%3Amtx%3Abook&rfr_id=info%3Asid/info%3Asid/zotero.org%3A2&rft.au=Jackson%2C+John&rft.place=%5BS.l.%5D&rft.date=1980&rft.btitle=Necessity+for+ruins%2C+and+other+topics.&rft.isbn=0870232924+9780870232923&ctx_ver=Z39.88-2004&rft.genre=book'
        b = from_openurl(q)
        self.assertTrue({'type': 'isbn', 'id': '9780870232923'} in b['identifier'])
        q = 'rft.isbn=0870232924&rft.isbn=9780870232923'
        b = from_openurl(q)
        self.assertTrue({'type': 'isbn', 'id': '0870232924'} in b['identifier'])

    def test_multiple_issn(self):
        q = 'rft.pub=Univ+Of+Mass+Press&r&rft.jtitle=Test&rft.issn=555+123&rft.genre=article'
        b = from_openurl(q)
        self.assertTrue({'type': 'issn', 'id': '555'} in b['identifier'])

    def test_author(self):
        q = 'sid=FirstSearch%3AWorldCat&genre=book&isbn=9780393066005&title=The+annotated+Peter+Pan&date=2011&aulast=Barrie&aufirst=J&auinitm=M&id=doi%3A&pid=%3Caccession+number%3E711051770%3C%2Faccession+number%3E%3Cfssessid%3E0%3C%2Ffssessid%3E%3Cedition%3E1st+ed.%2C+Centennial+ed.%3C%2Fedition%3E&url_ver=Z39.88-2004&rfr_id=info%3Asid%2Ffirstsearch.oclc.org%3AWorldCat&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&req_dat=%3Csessionid%3E0%3C%2Fsessionid%3E&rfe_dat=%3Caccessionnumber%3E711051770%3C%2Faccessionnumber%3E&rft_id=info%3Aoclcnum%2F711051770&rft_id=urn%3AISBN%3A9780393066005&rft.aulast=Barrie&rft.aufirst=J&rft.auinitm=M&rft.btitle=The+annotated+Peter+Pan&rft.date=2011&rft.isbn=9780393066005&rft.place=New+York&rft.pub=W.+W.+Norton+%26+Co.&rft.edition=1st+ed.%2C+Centennial+ed.&rft.genre=book&checksum=af5445c9c9a23c5e4fdbe11393dba00a'
        b = from_openurl(q)
        self.assertEqual(b['author'][0]['firstname'], 'J' ); self.assertEqual( type(b['author'][0]['firstname']), str)
        self.assertEqual(b['author'][0]['lastname'], 'Barrie' ); self.assertEqual( type(b['author'][0]['lastname']), str)
        self.assertEqual(b['author'][0]['name'], 'Barrie, J' ); self.assertEqual( type(b['author'][0]['name']), str)
        self.assertEqual(b['author'][0]['_minitial'], 'M' ); self.assertEqual( type(b['author'][0]['_minitial']), str)

    def test_eissn(self):
        q = 'eissn=15414159&date=2010-01-01&pages=125-141'
        b = from_openurl(q)
        self.assertTrue({'type': 'eissn', 'id': '15414159'} in b['identifier'])
        self.assertEqual(b['pages'], '125-141')

    def test_scholar_doi(self):
        q = 'sid=google&auinit=S&aulast=Maffeis&atitle=An+operational+semantics+for+JavaScript&id=doi:10.1007/978-3-540-89330-1_22'
        b = from_openurl(q)
        self.assertTrue(
            {
            'type': 'doi', 'id': 'doi:10.1007/978-3-540-89330-1_22'
            } in b['identifier']
        )

    def test_stitle(self):
        q = 'sid=tandf&genre=book&aulast=Buswell&date=1935&stitle=How+people+look+at+pictures%3A+A+study+of+the+psychology+of+perception+in+art&'
        b = from_openurl(q)
        self.assertEqual(b['title'], 'How people look at pictures: A study of the psychology of perception in art')
        #Also test if there is a short title and a full title, use title.
        q = 'title=Medical+studies&stitle=Med+studies'
        b = from_openurl(q)
        self.assertEqual(b['title'], 'Medical studies')

class TestThesisToOpenURL(unittest.TestCase):
    """
    Testing thesis and dissertations.  Pulled from logs May, 2014.
    """

    def test_a(self):
        #http://search.proquest.com/pqdtft/docview/1473656916/abstract
        q = 'ctx_ver=Z39.88-2004&ctx_enc=info:ofi/enc:UTF-8&rfr_id=info:sid/ProQuest+Dissertations+%26+Theses+Full+Text&rft_val_fmt=info:ofi/fmt:kev:mtx:dissertation&rft.genre=dissertations+%26+theses&rft.jtitle=&rft.atitle=&rft.au=Mangla%2C+Akshay&rft.aulast=Mangla&rft.aufirst=Akshay&rft.date=2013-01-01&rft.volume=&rft.issue=&rft.spage=&rft.isbn=&rft.btitle=&rft.title=Rights+for+the+Voiceless%3A+The+State%2C+Civil+Society+and+Primary+Education+in+Rural+India&rft.issn=&rft_id=info:doi/'
        b = from_openurl(q)
        self.assertEqual(b['title'], 'Rights for the Voiceless: The State, Civil Society and Primary Education in Rural India')
        self.assertEqual(b['type'], 'dissertation')
        self.assertEqual(b['author'][0]['name'], 'Mangla, Akshay')

    def test_b(self):
        q = u"""
?ctx_ver=Z39.88-2004&ctx_enc=info:ofi/enc:UTF-8&rfr_id=info:sid/ProQuest+Dissertations+%26+Theses+Full+Text&rft_val_fmt=info:ofi/fmt:kev:mtx:dissertation&rft.genre=dissertations+%26+theses&rft.jtitle=&rft.atitle=&rft.au=Grossman%2C+Robert+Allen&rft.aulast=Grossman&rft.aufirst=Robert&rft.date=1988-01-01&rft.volume=&rft.issue=&rft.spage=&rft.isbn=&rft.btitle=&rft.title=The+Lute+Suite+in+G+Minor+BWV+995+by+Johann+Sebastian+Bach%3A+A+comparison+of+the+autograph+manuscript+and+the+lute+intabulation+in+Leipzig%2C+Sammlung+Becker%2C+MS.+111.ii.3&rft.issn=&rft_id=info:doi/
"""
        b = from_openurl(q)
        self.assertTrue('Lute Suite in G Minor BWV 995 by Johann Sebastian Bach' in b['title'])
        self.assertEqual(b['type'], 'dissertation')
        self.assertEqual(b['year'], '1988')

    def test_c(self):
        q = u"""
ctx_ver=Z39.88-2004&rfr_id=info:sid/ProQuest+Dissertations+%26+Theses+Full+Text&rft_val_fmt=info:ofi/fmt:kev:mtx:dissertation&rft.genre=dissertations+%26+theses&rft.jtitle=&rft.atitle=&rft.au=Benjamin%2C+Ruha&rft.aulast=Benjamin&rft.aufirst=Ruha&rft.date=2008-01-01&rft.volume=&rft.issue=&rft.spage=&rft.isbn=9780549836568&rft.btitle=&rft.title=Culturing+consent%3A+Science+and+democracy+in+the+stem+cell+state&rft.issn=&rft_id=info:doi/
"""
        b = from_openurl(q)
        self.assertEqual(b['type'], 'dissertation')
        self.assertEqual(b['author'][0]['name'], 'Benjamin, Ruha')
        #ids
        ids = b['identifier']
        self.assertTrue(
            {
            'type': 'isbn', 'id': '9780549836568'
            } in ids
        )
        self.assertTrue(
            {
            'type': 'doi', 'id': 'doi:\n'
            } not in ids
        )

    def test_d(self):
        q = u"""
ctx_ver=Z39.88-2004&ctx_enc=info:ofi/enc:UTF-8&rfr_id=info:sid/ProQuest+Dissertations+%26+Theses+Full+Text&rft_val_fmt=info:ofi/fmt:kev:mtx:dissertation&rft.genre=dissertations+%26+theses&rft.jtitle=&rft.atitle=&rft.au=Ahuja%2C+Amit&rft.aulast=Ahuja&rft.aufirst=Amit&rft.date=2008-01-01&rft.volume=&rft.issue=&rft.spage=&rft.isbn=9780549979340&rft.btitle=&rft.title=Mobilizing+marginalized+citizens%3A+Ethnic+parties+without+ethnic+movements&rft.issn=&rft_id=info:doi/
"""
        b = from_openurl(q)
        self.assertEqual(b['type'], 'dissertation')
        self.assertEqual(b['author'][0]['name'], 'Ahuja, Amit')
        self.assertEqual(b['title'], 'Mobilizing marginalized citizens: Ethnic parties without ethnic movements')
        self.assertEqual(b['identifier'][0]['id'], '9780549979340')

class TestToOpenURL(unittest.TestCase):

    def test_book_chapter(self):
        q = 'sid=info:sid/sersol:RefinerQuery&genre=bookitem&isbn=9781402032899&&title=The+roots+of+educational+change&atitle=Finding+Keys+to+School+Change%3A+A+40-Year+Odyssey&volume=&part=&issue=&date=2005&spage=25&epage=57&aulast=Miles&aufirst=Matthew'
        b = from_openurl(q)
        ourl = to_openurl(b)
        qdict = parse_qs(ourl)
        self.assertTrue('bookitem' in qdict.get('rft.genre'))

    def test_missing_title(self):
        #Mock a sample request dict coming from Django.
        request_dict = {
        'rft.pub': ['Triple Canopy'],
        'rft_val_fmt': ['info:ofi/fmt:kev:mtx:book'],
        'rfr_id': ['info:sid/libx:brown'],
        'rft.au': ['Coleman,&#32;Gabriella'],
        'rft.aulast': ['Coleman'],
        'rft.aufirst': ['Gabriella'],
        'rft_id': ['http://canopycanopycanopy.com/15/our_weirdness_is_free'],
        'rft.btitle': ['Our Weirdness Is Free: The logic of Anonymous \u2014 online army, agent of chaos, and seeker of justice'],
        'url_ver': ['Z39.88-2004'],
        'rft.atitle': [''],
        'rft.genre': ['bookitem']}
        b = from_dict(request_dict)
        ourl = to_openurl(b)
        parsed_ourl = parse_qs(ourl)
        self.assertTrue('bookitem' in parsed_ourl.get('rft.genre'))
        self.assertTrue('Coleman, Gabriella' in parsed_ourl.get('rft.au'))

    def test_dissertation(self):
        request = {
            'ctx_enc': ['info:ofi/enc:UTF-8'],
            'ctx_ver': ['Z39.88-2004'],
            'rft.au': ['Mangla, Akshay'],
            'rft.aufirst': ['Akshay'],
            'rft.aulast': ['Mangla'],
            'rft.date': ['2013-01-01'],
            'rft.genre': ['dissertations & theses'],
            'rft.title': ['Rights for the Voiceless: The State, Civil Society and Primary Education in Rural India'],
            'rft_id': ['info:doi/'],
            'rft_val_fmt': ['info:ofi/fmt:kev:mtx:dissertation']
        }
        b = from_dict(request)
        ourl = to_openurl(b)
        parsed_ourl = parse_qs(ourl)
        self.assertTrue('dissertation' in parsed_ourl.get('rft.genre'))
        self.assertTrue('Rights for the Voiceless' in parsed_ourl.get('rft.title')[0])
        self.assertTrue('Mangla, Akshay') in parsed_ourl.get('rft.au')
        self.assertTrue('2013' in parsed_ourl.get('rft.date'))

class TestFromDict(unittest.TestCase):
    def test_throws_key_error(self):
        qdict = {'rfr_id': ['info:sid/libx'],
                 'rft.atitle': [''],
                 'rft.au': ['Coleman,&#32;Gabriella'],
                 'rft.aufirst': ['Gabriella'],
                 'rft.aulast': ['Coleman'],
                 'rft.btitle': ['Our Weirdness Is Free: The logic of Anonymous \\u2014 online army, agent of chaos, and seeker of justice'],
                 'rft.genre': ['bookitem'],
                 'rft.pub': ['Triple Canopy'],
                 'rft_id': ['http://canopycanopycanopy.com/15/our_weirdness_is_free'],
                 'rft_val_fmt': ['info:ofi/fmt:kev:mtx:book'],
                 'url_ver': ['Z39.88-2004']}
        b = from_dict(qdict)
        self.assertEqual(b['title'], 'Unknown')

def suite():
    suite1 = unittest.makeSuite(TestFromOpenURL, 'test')
    suite2 = unittest.makeSuite(TestToOpenURL, 'test')
    suite3 = unittest.makeSuite(TestFromDict, 'test')
    suite4 = unittest.makeSuite(TestThesisToOpenURL, 'test')
    all = unittest.TestSuite((suite1, suite2, suite3, suite4))
    return all

if __name__ == '__main__':
    unittest.main()
