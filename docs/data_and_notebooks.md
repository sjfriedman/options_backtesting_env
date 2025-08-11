### Data layout and notebooks

This repo contains raw daily EOD data files and cleaned parquet outputs used by the research notebooks.

Structure:

```
read_data/
  data/
    raw/      # Vendor-provided text files, organized by symbol and year/quarter
    clean/    # Parquet outputs ready for analysis
```

Examples in `raw/` include symbols like `AAPL`, `QQQ`, `SLV`, `SPY`, and `VIX`, partitioned by year or quarter folders with `.txt` files.

Cleaned outputs in `clean/` are parquet files per symbol, e.g. `AAPL.parquet`, `QQQ.parquet`, etc.


## Working with the notebooks

- `covered_call_leap.ipynb` (root) and notebooks under `backtest/` contain research for covered-call strategies and comparisons to benchmarks.
- `read_data/clean_data.ipynb` and `clean_data.ipynb` provide data cleaning and preparation steps.

Recommended environment:

```
python -m pip install jupyterlab pandas numpy matplotlib seaborn scipy scikit-learn pyarrow
jupyter lab
```

Tips:

- Ensure parquet readers find the files under `read_data/data/clean/` or adjust paths if you move them.
- Keep raw files in `read_data/data/raw/` out of version control if large; use `.gitignore` and/or external storage.


