bibjsontools_bul
================

Tools for working with [BibJSON](https://github.com/okfn/bibjson).

- This package's main focus is parsing an [OpenURL](http://en.wikipedia.org/wiki/OpenURL) and converting it to bibjson.

- There is also support for converting bibjson to an openurl.



#### notes ####

- Expects a unicode-string; if given a byte-string, will assume it's utf-8 and convert it to a unicode-string; all internal processing works on unicode-strings.

- Unicode handling...

    If there are unicode characters in the openurl, certain steps may be required to get desired results. Here is an example. Take the un-encoded openurl byte-string below.

        sid=FirstSearch%3AWorldCat&genre=book&title=Zen&date=1978&aulast=Yoshioka&aufirst=Tōichi&url_ver=Z39.88-2004&rfr_id=info%3Asid%2Ffirstsearch.oclc.org%3AWorldCat&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&rft.genre=book&req_dat=%3Csessionid%3E0%3C%2Fsessionid%3E&rfe_dat=%3Caccessionnumber%3E6104671%3C%2Faccessionnumber%3E&rft_id=info%3Aoclcnum%2F6104671&rft.aulast=Yoshioka&rft.aufirst=Tōichi&rft.btitle=Zen&rft.date=1978&rft.place=Osaka++Japan&rft.pub=Hoikusha&rft.edition=1st+ed.&rft.genre=book

    The first name there is `Tōichi`.

    Django's `request.META['QUERY_STRING']` will return a byte-string where, `aufirst=Tōichi` will be encoded to `aufirst=T%C5%8Dichi`.

    If that is passed directly to this package, it will be converted to a unicode-string, and the urlparse.parse_qs() will convert this to `{ u'aufirst': [u'T\xc5\x8dichi'] }`.

    Printing that unicode-string results in `TÅichi` -- _not_ desired.

    The following code is one solution...

        >>> from django.utils.encoding import uri_to_iri  # <https://docs.djangoproject.com/en/1.9/ref/unicode/#uri-and-iri-handling>
        >>> utf8_str = request.META['QUERY_STRING']  # produces byte-string `aufirst=T%C5%8Dichi`
        >>> unicode_str = uri_to_iri( utf8_str )  # produces unicode-string `aufirst=T\u014dichi` -- only updates unicode encoding
        >>> bib_dct = from_openurl( unicode_str )
        >>> print bib_dct['author'][0]['firstname']
        Tōichi



#### credit ###

Recent work is a speck on the shoulders of the great work done by [Ted Lawless](https://github.com/lawlesst) who created the [original bibjsontools](https://github.com/lawlesst/bibjsontools).

---
