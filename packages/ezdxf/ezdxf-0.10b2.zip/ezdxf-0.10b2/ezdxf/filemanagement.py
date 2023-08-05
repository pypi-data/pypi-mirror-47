# Purpose: DXF file testing and opening
# Created: 05.01.2018
# Copyright (C) 2018-2019, Manfred Moitzi
# License: MIT License
# Local imports to avoid cyclic import
from typing import TextIO, TYPE_CHECKING, Union, Sequence
from ezdxf.tools.standards import setup_drawing
from ezdxf.lldxf.const import DXF12, DXF2013
from ezdxf.drawing import Drawing

if TYPE_CHECKING:
    from ezdxf.eztypes import DXFInfo


def new(dxfversion: str = DXF2013, setup: Union[str, bool, Sequence[str]] = None) -> 'Drawing':
    """
    Create a new DXF drawing.

    new() can create drawings for following DXF versions:

    - AC1009 or R12: AutoCAD R12 (DXF R12)
    - AC1015 or R2000: AutoCAD 2000 (DXF R2000)
    - AC1018 or R2004: AutoCAD 2004 (DXF R2004)
    - AC1021 or R2007: AutoCAD 2007 (DXF R2007)
    - AC1024 or R2010: AutoCAD 2010 (DXF R2010)
    - AC1027 or R2013: AutoCAD 2013 (DXF R2013)
    - AC1032 or R2018: AutoCAD 2018 (DXF R2018)

    Args:
        dxfversion: DXF version specifier as string, default is R2013
        setup: setup drawing standard for linetypes, text styles, dimension styles
               - None or False: no setup
               - 'all' or True: setup all

               list of topics as strings:

                  - 'linetypes' ... setup line types
                  - 'styles'  ... setup text styles
                  - 'dimstyles ... setup all dimension styles
                  - 'dimstyles:metric' ... setup metric dimension styles
                  - 'dimstyles:imperial' ... setup imperial dimension styles (not implemented yet)
                  - 'visualstyles ... setup 25 standard visual styles

    """
    doc = Drawing.new(dxfversion)
    if setup:
        setup_drawing(doc, topics=setup)
    return doc


def read(stream: TextIO, legacy_mode: bool = False, filter_stack=None) -> 'Drawing':
    """
    Read DXF drawing from a text stream, which only needs a readline() method.

    Supported DXF versions:

    - pre AC1009 DXF versions will be upgraded to AC1009, requires encoding set by header var $DWGCODEPAGE
    - AC1009: AutoCAD R12 (DXF R12), requires encoding set by header var $DWGCODEPAGE
    - AC1012: AutoCAD R13 upgraded to AC1015, requires encoding set by header var $DWGCODEPAGE
    - AC1014: AutoCAD R14 upgraded to AC1015, requires encoding set by header var $DWGCODEPAGE
    - AC1015: AutoCAD 2000, requires encoding set by header var $DWGCODEPAGE
    - AC1018: AutoCAD 2004, requires encoding set by header var $DWGCODEPAGE
    - AC1021: AutoCAD 2007, requires encoding='utf-8'
    - AC1024: AutoCAD 2010, requires encoding='utf-8'
    - AC1027: AutoCAD 2013, requires encoding='utf-8'
    - AC1032: AutoCAD 2018, requires encoding='utf-8'

    To detect the required encoding, use the helper function info=dxf_stream_info(stream)
    and reopen the stream with the detected info.encoding.

    Args:
        stream: input text stream opened with correct encoding, requires only a readline() method.
        legacy_mode:  True - adds an extra trouble shooting import layer; False - requires DXF file created by a modern
            CAD application
        filter_stack: interface to put filters between reading layers, see :class:`Drawing.read` for more information

    """
    from ezdxf.drawing import Drawing

    return Drawing.read(stream, legacy_mode=legacy_mode, filter_stack=filter_stack)


def readfile(filename: str, encoding: str = None, legacy_mode: bool = False, filter_stack=None) -> 'Drawing':
    """
    Read DXF drawing specified by *filename* from file system.

    Supported DXF versions:

    - pre AC1009 DXF versions will be upgraded to AC1009
    - AC1009: AutoCAD R12 (DXF R12)
    - AC1012: AutoCAD R13 upgraded to AC1015
    - AC1014: AutoCAD R14 upgraded to AC1015
    - AC1015: AutoCAD 2000
    - AC1018: AutoCAD 2004
    - AC1021: AutoCAD 2007, fixates encoding='utf-8'
    - AC1024: AutoCAD 2010, fixates encoding='utf-8'
    - AC1027: AutoCAD 2013, fixates encoding='utf-8'
    - AC1032: AutoCAD 2018, fixates encoding='utf-8'

    Args:
        filename: DXF filename
        encoding: use None for auto detect, or set a specific encoding like 'utf-8'
        legacy_mode: True - adds an extra trouble shooting import layer; False - requires DXF file from modern CAD apps
        filter_stack: interface to put filters between reading layers, see :class:`Drawing.read` for more information

    """
    from ezdxf.lldxf.validator import is_dxf_file
    from ezdxf.tools.codepage import is_supported_encoding

    if not is_dxf_file(filename):
        raise IOError("File '{}' is not a DXF file.".format(filename))

    info = dxf_file_info(filename)
    with open(filename, mode='rt', encoding=info.encoding, errors='ignore') as fp:
        doc = read(fp, legacy_mode=legacy_mode, filter_stack=filter_stack)

    doc.filename = filename
    if encoding is not None and is_supported_encoding(encoding):
        doc.encoding = encoding
    return doc


def dxf_file_info(filename: str) -> 'DXFInfo':
    """
    Reads basic file information from DXF files: DXF version, encoding and handle seed.

    Returns:
        DXF info object with attributes: version, release, handseed, encoding

    """
    with open(filename, mode='rt', encoding='utf-8', errors='ignore') as fp:
        return dxf_stream_info(fp)


def dxf_stream_info(stream: TextIO) -> 'DXFInfo':
    """
    Reads basic DXF information from a text stream: DXF version, encoding and handle seed.

    Returns:
        DXF info object with attributes: version, release, handseed, encoding

    """
    from ezdxf.lldxf.tags import dxf_info

    info = dxf_info(stream)
    if info.version >= 'AC1021':  # R2007 files and later are always encoded as UTF-8
        info.encoding = 'utf-8'
    return info


def readzip(zipfile: str, filename: str = None) -> 'Drawing':
    """
    Read DXF drawing specified by filename from a zip archive, or if filename is None the first DXF file in the zip
    archive.

    Supported DXF versions:

    - pre AC1009 DXF versions will be upgraded to AC1009
    - AC1009: AutoCAD R12 (DXF12)
    - AC1012: AutoCAD R13 upgraded to AC1015
    - AC1014: AutoCAD R14 upgraded to AC1015
    - AC1015: AutoCAD 2000
    - AC1018: AutoCAD 2004
    - AC1021: AutoCAD 2007
    - AC1024: AutoCAD 2010
    - AC1027: AutoCAD 2013
    - AC1032: AutoCAD 2018

    Args:
        zipfile: name of the zip archive
        filename: filename of DXF file, or None to read the first DXF file from the zip archive.

    """
    from ezdxf.tools.zipmanager import ctxZipReader

    with ctxZipReader(zipfile, filename) as zipstream:
        dwg = read(zipstream)
        dwg.filename = zipstream.dxf_file_name
    return dwg
