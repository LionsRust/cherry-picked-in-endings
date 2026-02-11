# Cherry-Picked In Endings

Web app to browse and filter **surnames ending in -in** only. Data is ranked by popularity from US Census and Russian surname lists. Same app as [Cherry-Picked Surnames](https://github.com/your-org/Cherry-Picked-Surnames), different filter.

## Generate the list

Run the build script with the same CSV/txt files you use for the main list:

```bash
# Two files: US/combined census, then Russian list
python3 build_in.py path/to/census.csv path/to/russian.csv

# Or one combined file with columns: surname, count_combined, count_russian
python3 build_in.py path/to/combined.csv
```

Output is `surnames_filtered_in.json` in this folder. Without arguments, the script writes an empty list.

## Run locally

Serve the folder over HTTP (required for loading the JSON):

```bash
python3 -m http.server 8000
```

Then open **http://localhost:8000** and click **index.html**.

## Filters

- **Search** — filter by substring
- **Russian** — All / Russian only / Not Russian

Favourites and deleted lists are stored in `localStorage` under `surname-in-favourites` and `surname-in-deleted`.
