

# Bits and bytes #

## MusicBrainz webinterface tagger integration ##
```
>>> import socket
>>> HOST = ''
>>> PORT = 8000
>>> s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
>>> s.bind((HOST, PORT))
>>> s.listen(1)
>>> conn, addr = s.accept()
>>> print 'Connected by', addr
Connected by ('127.0.0.1', 52401)
>>> while 1:
...   data = conn.recv(1024)
...   if not data: break
...   print data
... 
```

Which would result in something like this:
```
GET /openalbum?id=e7635d5c-988a-430c-b2d8-de25e5d0e068&t=1303225591172 HTTP/1.1
Host: 127.0.0.1:8000
Connection: keep-alive
Referer: http://musicbrainz.org/search/textsearch.html?type=release&query=beets&tport=8000
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.44 Safari/534.24
Accept: application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5
Accept-Encoding: gzip,deflate,sdch
Accept-Language: en-US,en;q=0.8,nl;q=0.6,fr;q=0.4,en-GB;q=0.2
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3
```

# Links to keep track of #
  * http://www.id3.org/iTunes_Normalization_settings
  * http://atomicparsley.sourceforge.net/mpeg-4files.html
  * http://www.mp4ra.org/atoms.html
  * http://www.iso.org/iso/iso_catalogue/catalogue_tc/catalogue_detail.htm?csnumber=38538
  * http://flac.sourceforge.net/format.html
  * http://www.id3.org/id3v2.3.0
  * http://www.id3.org/id3v2.4.0-frames
  * http://wiki.multimedia.cx/index.php?title=MP4#Meta_Data
  * http://code.google.com/p/php-reader/
  * http://www.geocities.com/xhelmboyx/quicktime/formats/mp4-layout.txt  << Yahoo terminated GeoCities, we need to find a copy of that txt

## Vorbis Comments standards ##
  * [modern album art standard](http://wiki.xiph.org/VorbisComment#METADATA_BLOCK_PICTURE)
  * [picard's implementation thereof](http://musicbrainz.1054305.n4.nabble.com/Branch-musicbrainz-developers-picard-trunk-Rev-1018-Use-new-METADATA-BLOCK-PICTURE-tag-to-store-cove-td1093752.html) (as a diff from a version using the old COVERART format)
  * [Quod Libet's implementation](http://code.google.com/p/quodlibet/source/browse/quodlibet/quodlibet/formats/xiph.py#63) of the same (read-only)