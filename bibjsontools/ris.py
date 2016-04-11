# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Convert from BibJSON to RIS file-format
- [BibJSON]( http://okfnlabs.org/bibjson/ )
- [RIS]( https://en.wikipedia.org/wiki/RIS_(file_format) )
Adapted from <https://github.com/okfn/bibserver/blob/master/parserscrapers_plugins/RISParser.py>
"""

from bibjsontools import from_openurl


class RISMaker( object ):

    def __init__(self):
        self.FIELD_MAP = {
            'access date': 'Y2',
            'accession number': 'AN',
            'alternate title': 'J2',
            'author': 'AU',
            'call number': 'CN',
            'caption': 'CA',
            'custom 3': 'C3',
            'custom 4': 'C4',
            'custom 5': 'C5',
            'custom 7': 'C7',
            'custom 8': 'C8',
            'database provider': 'DP',
            'date': 'DA',
            'doi': 'DO',
            'epub date': 'ET',
            'figure': 'L4',
            'file attachments': 'L1',
            'institution': 'AD',
            'issn': 'SN',
            'issue': 'IS',
            'journal': 'JF',
            'keyword': 'KW',
            'label': 'LB',
            'language': 'LA',
            'name of database': 'DB',
            'nihmsid': 'C6',
            'note': 'AB',
            'notes': 'N1',
            'number': 'IS',
            'number of volumes': 'NV',
            'original publication': 'OP',
            'pages': 'SP',
            'place published': 'CY',
            'pmcid': 'C2',
            'publisher': 'PB',
            'reprint edition': 'RP',
            'reviewed item': 'RI',
            'secondary title': 'T2',
            'section': 'SE',
            'short title': 'ST',
            'start page': 'M2',
            'subsidiary author': 'A4',
            'tertiary author': 'A3',
            'tertiary title': 'T3',
            'title': 'TI',
            'translated author': 'TA',
            'translated title': 'TT',
            'type ': 'TY',
            'url': 'UR',
            'volume': 'VL',
            'year': 'PY'
            }

    def convert_to_ris( self, bib_dct ):
        """ Converts bibjson data to ris data. """
        ris_dct = {}
        ris_dct['TY'] = self._handle_type( bib_dct['type'] )
        for k,v in bib_dct.items():
            if k == 'author':
                ris_dct = self._check_author( ris_dct, v )
            elif k == 'journal':
                ris_dct['JF'] = v.get('name')
            elif k == 'identifier':
                ris_dct = self._check_identifier( ris_dct, v )
            else:
                ris_k = FIELD_MAP.get(k, None)
                if ris_k:
                    ris_v = bib_dct.get(k)
                    ris_dct[ris_k] = ris_v
        return ris_dct

    def _handle_type( self, item_type ):
        """ Updates ris_dct['TY'].
            Called by convert_to_ris() """
        if item_type == 'article':
            ris_type = 'JOUR'
        elif item_type == 'book':
            ris_type = 'BOOK'
        else:
            ris_type = 'GENERIC'
        return ris_type

    def _check_author( self, ris_dct, author_list ):
        """ Checks author value (a list of dcts).
            Called by convert_to_ris() """
        for author in author_list:
            name = author.get( 'name' )
            if name:
                ris_dct['AU'] = name
                break
        return ris_dct

    def _check_identifier( self, ris_dct, identifier_list ):
        """ Checks identifier value (a list of dcts).
            Called by convert_to_ris() """
        for identifier_dct in identifier_list:
            id_value = identifier_dct['id']
            if identifier_dct['type'] == 'doi':
                ris_dct['DO'] = id_value
            elif identifier_dct['type'] == 'issn':
                ris_dct['SN'] = id_value
            elif identifier_dct['type'] == 'isbn':
                ris_dct['SN'] = id_value
        return ris_dct

    # def convert_to_ris( self, bib_dct ):
    #     """ Converts bibjson data to ris data. """
    #     ris_dct = {}
    #     ris_dct['TY'] = self._handle_type( bib_dct['type'] )
    #     for k,v in bib_dct.items():
    #         if k == 'author':
    #             ris_dct = self._check_author( ris_dct, v )
    #         elif k == 'journal':
    #             ris_dct['JF'] = v.get('name')
    #         elif k == 'identifier':
    #             for idt in v:
    #                 this = idt['id']
    #                 if idt['type'] == 'doi':
    #                     ris_dct['DO'] = this
    #                 elif idt['type'] == 'issn':
    #                     ris_dct['SN'] = this
    #                 elif idt['type'] == 'isbn':
    #                     ris_dct['SN'] = this
    #                 #elif idt['type'] == 'pmid':
    #                 #   ris_dct[]
    #         else:
    #             ris_k = FIELD_MAP.get(k, None)
    #             if ris_k:
    #                 ris_v = bib_dct.get(k)
    #                 ris_dct[ris_k] = ris_v
    #     return ris_dct

    # end class RISMaker()


FIELD_MAP = {
	'access date': 'Y2',
	'accession number': 'AN',
	'alternate title': 'J2',
	'author': 'AU',
	'call number': 'CN',
	'caption': 'CA',
	'custom 3': 'C3',
	'custom 4': 'C4',
	'custom 5': 'C5',
	'custom 7': 'C7',
	'custom 8': 'C8',
	'database provider': 'DP',
	'date': 'DA',
	'doi': 'DO',
	'epub date': 'ET',
	'figure': 'L4',
	'file attachments': 'L1',
	'institution': 'AD',
	'issn': 'SN',
	'issue': 'IS',
	'journal': 'JF',
	'keyword': 'KW',
	'label': 'LB',
	'language': 'LA',
	'name of database': 'DB',
	'nihmsid': 'C6',
	'note': 'AB',
	'notes': 'N1',
	'number': 'IS',
	'number of volumes': 'NV',
	'original publication': 'OP',
	'pages': 'SP',
	'place published': 'CY',
	'pmcid': 'C2',
	'publisher': 'PB',
	'reprint edition': 'RP',
	'reviewed item': 'RI',
	'secondary title': 'T2',
	'section': 'SE',
	'short title': 'ST',
	'start page': 'M2',
	'subsidiary author': 'A4',
	'tertiary author': 'A3',
	'tertiary title': 'T3',
	'title': 'TI',
	'translated author': 'TA',
	'translated title': 'TT',
	'type ': 'TY',
	'url': 'UR',
	'volume': 'VL',
	'year': 'PY'
}

def convert(bib):
	"""
	Convert BibJSON to the RIS format for import into various utilities.
	To do: add some test cases.
	"""
	ris = {}
	if bib['type'] == 'article':
		ris['TY'] = 'JOUR'
	elif bib['type'] == 'book':
		ris['TY'] = 'BOOK'
	else:
		ris['TY'] = 'GENERIC'

	for k,v in bib.items():
		if k == 'author':
			for author in v:
				name = author.get('name')
				if name:
					ris['AU'] = name
		elif k == 'journal':
			ris['JF'] = v.get('name')
		elif k == 'identifier':
			for idt in v:
				this = idt['id']
				if idt['type'] == 'doi':
					ris['DO'] = this
				elif idt['type'] == 'issn':
					ris['SN'] = this
				elif idt['type'] == 'isbn':
					ris['SN'] = this
				#elif idt['type'] == 'pmid':
				#	ris[]
		else:
			ris_k = FIELD_MAP.get(k, None)
			if ris_k:
				ris_v = bib.get(k)
				ris[ris_k] = ris_v

	out = ''
	for k,v in ris.items():
		out += '%s  - %s\n' % (k, v)
	return out
