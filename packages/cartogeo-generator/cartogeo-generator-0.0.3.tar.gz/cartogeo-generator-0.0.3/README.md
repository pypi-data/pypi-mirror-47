# Cartogeo

## Map Image
Generate an image of a map between two points
```bash
python -m cartogeo.map NH9506 NO1090 output.png
python -m cartogeo.map NH9506 NO1090 output.png --25k

python -m cartogeo.map NH0128 NH1521 output.png
python -m cartogeo.map NH0128 NH1520 output.png --25k
python -m cartogeo.map NH008282 NH152198 output.png

python -m cartogeo.map NC0000 NO0000 output.png --250k
```

## Map Printout
```bash
python -m cartogeo.pdf NH0128 output.pdf
python -m cartogeo.pdf NH012278 output.pdf
python -m cartogeo.pdf NH0128 output.pdf --portrait --25k
python -m cartogeo.pdf NH012278 output.pdf --portrait --25k
```

## Map Data Path
```bash
MAP_DATA_PATH
```

