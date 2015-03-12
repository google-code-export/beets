# Introduction #

MediaFile is a Python class that can be used for high-level, abstract operations on the metadata of music files. It is an abstraction layer on top of the excellent [Mutagen](http://www.sacredchao.net/quodlibet/wiki/Development/Mutagen) tagging library, which handles low-level interaction with metadata tags. It intends to present a uniform API independent of file format and robustly support the possible quirks introduced by other taggers.

It currently supports MP3 files (ID3 tags), AAC files (as tagged by iTunes) as well as FLAC, Ogg, Monkey's Audio, WavPack, and Musepack. It performs well under our tests but will likely need improvement when it deals with the full variety of quirky tags "in the wild." We're comfortable with this and will take a case-by-case approach to improving its interoperability with other applications.

MediaFile attempts to always return a usable value (i.e., it never returns None or throws an exception when a tag is accessed). If a tag is not present, an empty and false value of the appropriate type -- such as zero or the empty string -- is returned.

# Usage #

```
>>> f = MediaFile('Lucy.mp3')
>>> f.title
u'Lucy in the Sky with Diamonds'
>>> f.artist = 'The Beatles'
>>> f.save()
```

# Supported Metadata Fields #

  * `title`
  * `artist`
  * `album`
  * `genre`
  * `composer`
  * `grouping`
  * `year` (of release)
  * `month`
  * `day`
  * `date` (`datetime.date(year, month, day`)
  * `track` (track number)
  * `tracktotal` (number of tracks on the release)
  * `disc`
  * `disctotal`
  * `lyrics`
  * `comments`
  * `bpm` (tempo)
  * `comp` (is it a compilation?)
  * `bitrate` (read-only, an integral number of bits)
  * `length` (read-only, a real number of seconds)
  * `art` (album art; see below)

Note that the `day` field may not be used if `month` isn't set (or, equivalently, is zero) and that `month` isn't usable if `year` isn't set. This is because of storage details but kind of makes sense. Also, the `date` field is just a convenient way to access the component `year`, `month`, and `day` fields. It is a `datetime.date` object indicating the smallest valid date whose components are at least as large as the three component fields (that is, if `year == 1999`, `month == 0`, and `day == 0`, then `date == datetime.date(1999, 1, 1)`). If the components indicate an invalid date (e.g., if `month == 47`), `datetime.date.min` is returned. Obviously, setting the `date` field sets the three component fields.

# Album Art #

The `art` field is a little bit different. It can be either `None` (indicating no art at all) or a `(data, kind)` tuple. `data` is a bytesting containing the image data and `kind` indicates the image codec. It's an instance of the `imagekind` enum, which is either `JPEG` or `PNG`. These two are the only supported formats because they are the only ones that can be supported across all audio metadata formats: MPEG-4 only supports PNG and JPEG.

# Compatibility #

The ID3 and MPEG-4 test cases were created with iTunes and the FLAC and Ogg test cases were created (mostly) with [MediaRage](http://www.chaoticsoftware.com/ProductPages/MediaRage.html). The Monkey's Audio tags were mainly fabricated using the open-source [Tag](http://sbooth.org/Tag/). Thus, MediaFile's tag support most closely aligns with those three applications. Some open questions remain about how to most compatibly tag files. In particular, some fields MediaFile supports don't seem standardized among FLAC/Ogg taggers:

  * `grouping` and `lyrics`: couldn't find anyone who supports these in a cursory search; MediaFile uses the keys `grouping` and `lyrics`
  * `tracktotal` and `disctotal`: we use the keys `tracktotal`, `totaltracks`, and `trackc` all to mean the same thing
  * `year`: this field appears both as a part of the `date` field and on its own using some taggers; both are supported

For fields that have multiple possible storage keys, MediaFile optimizes for interoperability: it accepts _any_ of the possible storage keys and writes _all_ of them. This may result in duplicated information in the tags, but it ensures that other players with slightly divergent opinions on tag names will all be able to interact with beets.

For a (marginally readable) list of the ways various fields are interpreted and stored by MediaFile, see the very end of [mediafile.py](http://code.google.com/p/beets/source/browse/trunk/beets/mediafile.py).

Images (album art) are stored in the standard ways for ID3 and MPEG-4. For all other formats, images are stored with the [METADATA\_BLOCK\_PICTURE standard](http://wiki.xiph.org/VorbisComment#METADATA_BLOCK_PICTURE) from Vorbis Comments. The older [COVERART unofficial format](http://wiki.xiph.org/VorbisComment#Unofficial_COVERART_field_.28deprecated.29) is also read but is not written.