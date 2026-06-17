import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import os, json
sys.path.insert(0, "C:/Program Files/QGIS 3.44.11/apps/Python312/Lib/site-packages")
from osgeo import ogr, osr

INFILE = "C:/Users/47433/OneDrive - KTH/MasterThesis OneDrive/Extension study permit/geodata/svenska_landskap.geojson"
OUTFILE = "C:/Users/47433/OneDrive - KTH/MasterThesis OneDrive/Extension study permit/geodata/province_paths.json"

SVG_W = 500
SVG_H = 900
PAD   = 18

ds    = ogr.Open(INFILE)
layer = ds.GetLayer(0)

# SWEREF99 TM (EPSG:3006) is Sweden's native flat projection — perfect for this
src = osr.SpatialReference(); src.ImportFromEPSG(4326)
# Force traditional GIS axis order (Lon,Lat) and (Easting,Northing) on BOTH SRS.
# GDAL 3.x defaults to authority axis order which swaps these, causing 90° rotation.
src.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
tgt = osr.SpatialReference(); tgt.ImportFromEPSG(3006)
tgt.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
t   = osr.CoordinateTransformation(src, tgt)

features_data = []
all_x, all_y  = [], []

layer.ResetReading()
for feat in layer:
    g = feat.GetGeometryRef().Clone()
    g.Transform(t)
    s = g.Simplify(5000)  # 5 km tolerance — still very accurate visually
    e = s.GetEnvelope()
    all_x += [e[0], e[1]]
    all_y += [e[2], e[3]]
    features_data.append(({
        "landskap":     feat.GetField("landskap"),
        "landsdel":     feat.GetField("landsdel"),
        "landsdelskod": feat.GetField("landsdelskod"),
    }, s))

print(f"X: {min(all_x):.0f} – {max(all_x):.0f}")
print(f"Y: {min(all_y):.0f} – {max(all_y):.0f}")

mx, Mx = min(all_x), max(all_x)
my, My = min(all_y), max(all_y)

mw = SVG_W - 2*PAD
mh = SVG_H - 2*PAD
sc = min(mw / (Mx-mx), mh / (My-my))

ox = PAD + (mw - sc*(Mx-mx))/2
oy = PAD + (mh - sc*(My-my))/2

def to_svg(px, py):
    # In SWEREF99 TM: X = easting (west→east), Y = northing (south→north)
    # SVG: x goes left→right (matches easting), y goes top→bottom (flip northing)
    sx = ox + (px - mx) * sc
    sy = SVG_H - (oy + (py - my) * sc)
    return round(sx, 1), round(sy, 1)

def ring_d(ring):
    pts = []
    for i in range(ring.GetPointCount()):
        x, y, *_ = ring.GetPoint(i)
        sx, sy = to_svg(x, y)
        pts.append(f"{sx},{sy}")
    return ("M " + " L ".join(pts) + " Z") if pts else ""

def geom_d(g):
    n = g.GetGeometryName()
    parts = []
    if n == "POLYGON":
        for i in range(g.GetGeometryCount()):
            s = ring_d(g.GetGeometryRef(i))
            if s: parts.append(s)
    elif n in ("MULTIPOLYGON","GEOMETRYCOLLECTION"):
        for i in range(g.GetGeometryCount()):
            parts.append(geom_d(g.GetGeometryRef(i)))
    return " ".join(p for p in parts if p)

def centroid_svg(g):
    c = g.Centroid()
    return to_svg(c.GetX(), c.GetY())

output = {"viewBox": f"0 0 {SVG_W} {SVG_H}", "provinces": []}
for props, g in features_data:
    d  = geom_d(g)
    cx, cy = centroid_svg(g)
    pid = props["landskap"].lower().replace("\u00e5","a").replace("\u00e4","a").replace("\u00f6","o").replace(" ","_")
    output["provinces"].append({
        "id": pid, "name": props["landskap"],
        "landsdel": props["landsdel"], "landsdelskod": props["landsdelskod"],
        "path": d, "cx": cx, "cy": cy
    })
    print(f"  {props['landskap']:20s}  cx={cx:6.1f} cy={cy:6.1f}  path={len(d)} chars")

with open(OUTFILE, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nDone: {OUTFILE}")
