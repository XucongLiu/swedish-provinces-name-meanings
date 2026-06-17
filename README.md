# Swedish Provinces — Literal Name Meanings

An interactive map of Sweden's 25 historical provinces (*landskap*) that reveals the **literal etymological meaning** of each province's name.

👉 **[Open the map](sweden_provinces_map.html)** — works offline, no server needed.

![Map preview](geodata/preview.png)

## Features

- 🗺 **Accurate geographic boundaries** — official Lantmäteriet data (CC0)
- 🖱 **Hover** any province → tooltip shows its literal meaning instantly
- 🖱 **Click** any province → full etymology card in the sidebar
- 🔍 **Search box** to filter all 25 provinces by name or meaning
- 🔎 **Zoom & pan** — scroll wheel, +/− buttons, click-drag
- 📱 **Touch pinch-zoom** support

## Province Name Origins

| Province | Literal Meaning |
|---|---|
| Skåne | Scandinavia's Origin / Hazardous Shore |
| Blekinge | The Shining / Pale Land |
| Öland | Island Land |
| Halland | Stony Slopes |
| Småland | Small Lands |
| Gotland | Land of the Gutar |
| Västergötland | West Gothland |
| Östergötland | East Gothland |
| Bohuslän | District of Bohus Fortress |
| Dalsland | Valley Land |
| Närke | The Narrow One |
| Södermanland | Land of the Southern Men |
| Värmland | Land of the Warm-River Folk |
| Västmanland | Land of the Western Men |
| Uppland | The Up-Land |
| Gästrikland | Land of the Guests |
| Dalarna | The Valleys |
| Hälsingland | Land of the Neck-Dwellers |
| Härjedalen | Valley of the Härje River |
| Medelpad | Middle Path |
| Ångermanland | Land of the Narrow Fjords |
| Jämtland | Land of the Jämtar People |
| Västerbotten | West Bothnian Region |
| Lappland | Land of the Sámi People |
| Norrbotten | North Bothnian Region |

## Technical Details

- **No dependencies** — pure HTML + CSS + JavaScript, works offline
- **Geographic data**: [perliedman/svenska-landskap](https://github.com/perliedman/svenska-landskap) (Lantmäteriet, CC0 licence)
- **Projection**: SWEREF99 TM (EPSG:3006) — Sweden's official national coordinate system
- **Processing**: QGIS 3.44 / GDAL OGR — reprojection + 5 km simplification
- **Styling**: Dark theme, Google Fonts (Outfit + Playfair Display)

## Regenerating the Map

Requires [QGIS](https://qgis.org/) (tested with 3.44).

```powershell
# Step 1 — Convert GeoJSON → SVG path data
& "C:\Program Files\QGIS 3.44.11\bin\python.exe" geodata/generate_svg_paths.py

# Step 2 — Build the HTML map
& "C:\Program Files\QGIS 3.44.11\bin\python.exe" geodata/build_map.py
```

## File Structure

```
├── sweden_provinces_map.html   ← The interactive map (open this!)
├── README.md
├── .gitignore
└── geodata/
    ├── svenska_landskap.geojson   ← Official province boundaries (CC0)
    ├── province_paths.json        ← Generated SVG path data
    ├── generate_svg_paths.py      ← Script: GeoJSON → SVG paths
    └── build_map.py               ← Script: SVG paths + data → HTML
```

## Licence

- Map code: MIT
- Geographic data: [CC0](https://creativecommons.org/publicdomain/zero/1.0/) (Lantmäteriet via perliedman/svenska-landskap)
