#!/usr/bin/env python
from argparse import ArgumentParser
import json

version = '0.1'

def read_lines_txt(filename):
    constellations = {}
    with open(filename, 'r', encoding="utf-8") as f:
        abbr = None
        polylines = None
        for l in f:
            l = l.strip()
            if l == "" or l.startswith('#'):
                continue
            if l.endswith(':'):
                abbr = l[0:-1]
                polylines = []
                constellations[abbr] = polylines
                continue
            # polyline-string -> points
            points = list(map(lambda p: p.strip(), l.split(sep='-')))
            polylines.append(points)
    return constellations

def get_stars(polylines):
    star_dict = {}
    # polylines -> stars
    for points in polylines:
        for p in points:
            if p in star_dict:
                continue
            star_dict[p] = True
    return list(star_dict.keys())
    
def query_stars(abbr, stars):
    from astroquery.simbad import Simbad
    from astropy import units as u
    from astropy.coordinates import SkyCoord
    Simbad.TIMEOUT = 120
    table = Simbad.query_objects(map(lambda s: s + ' ' + abbr, stars))
    # print(table)
    coord_dict = {}
    for i, r in enumerate(table):
        c = SkyCoord(r['RA'], r['DEC'], unit=(u.hourangle, u.deg), frame="icrs")
        coord_dict[stars[i]] = (str(c.ra.hour), str(c.dec.deg))
        # print(stars[i] + ": " + str(coord_dict[stars[i]]))
    return coord_dict

def get_constellation_lines(constellations):
    lines = []
    for abbr in constellations.keys():
        stars = get_stars(constellations[abbr])
        # print(abbr + ": " + str(stars))
        coord_dict = query_stars(abbr, stars)
        for polyline in constellations[abbr]:
            coord_objs = []
            pol = {}
            pol['pol'] = coord_objs
            pol['c'] = abbr.upper()
            lines.append(pol)
            for star in polyline:
                coord = coord_dict[star]
                coord_obj = {}
                coord_obj['x'] = float(coord[0])
                coord_obj['y'] = float(coord[1])
                coord_objs.append(coord_obj)
    return lines

argparser = ArgumentParser(description='Gerenate ConstellationLines.json for '\
                           'PixInsight\'s AnnotateImage '\
                           'from simple definition file.')
argparser.add_argument('lines_txt', metavar='lines.txt',
                       help='source file: '\
                       'constellation lines definition file.')
argparser.add_argument('constellationlines_json',
                       metavar='ConstellationLines.json',
                       help='destination file: '\
                       'constellation lines config file for AnnotateImage.')
argparser.add_argument("-m", "--merge-to-destination", action="store_true",
                       help="merge output to destination file.")

argparser.add_argument('--version', action='version',
                       version='%(prog)s ' + version)
args = argparser.parse_args()

constellations = read_lines_txt(args.lines_txt)
# print(json.dumps(constellations, indent=2, ensure_ascii=False))
constellations_lines = get_constellation_lines(constellations)
# print(constellations_lines)
dest_lines = constellations_lines
if args.merge_to_destination:
    abbr_dict = {}
    for abbr in constellations.keys():
        abbr_dict[abbr.upper()] = True
    with open(args.constellationlines_json, 'r', encoding="utf-8") as f:
        dest_lines = json.load(f)
        for line in dest_lines[:]:
            if line['c'].upper() in abbr_dict:
                dest_lines.remove(line)
        for line in constellations_lines:
            dest_lines.append(line)

with open(args.constellationlines_json, 'w', encoding="utf-8") as f:
    json.dump(dest_lines, f, indent=0)
