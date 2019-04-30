# Try Block Data in SQLite3

## Installation

Using `conda`:

`conda install --yes --file requirements.txt`

Using `pip`

`pip install -r requirements.txt`

OR convenience commands from `Hoffmann`:
[Install only available packages using “conda install --yes --file requirements.txt” without error](https://stackoverflow.com/a/38609653/741197)

`while read requirement; do conda install --yes $requirement || pip install $requirement; done < requirements.txt`

## Usage

`python3 main.py`

## Results

### On Laptop

**Summary**:

- Average Fetch: `5s`
- Average Insert: `44ms`

```sh
Requet date: [29, 30]

Fetch Schedule Blocks At Date 

https://neuraldisplay-admin-api.herokuapp.com/test/blocks?days=29&days=30
200
fetch_data --- 5.0221428871154785 seconds ---
insert_data --- 0.04486203193664551 seconds ---
Recurrence request --- 72.51000761985779 seconds ---

Get Schedule Blocks At Date: 3
5760
get_schedule --- 0.04164695739746094 seconds ---

------- Check and print all metrics again -------

Entire database contents:

[('data',)]
172800
--- 0.016084909439086914 seconds ---
(sqlite-db)
```

### On Raspi

**Summary**:

- Average Fetch: `4s`
- Average Insert: `240 ms`

On Raspi insert data slower `240 ms / 40ms = 6` times