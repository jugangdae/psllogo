# PSL PNG Logo

It converts the SVG logos in the `svg/` folder into square PNG logos.

## Setup

Just run `./run.sh`. It automatically creates `.venv` and installs the required packages.

Python 3 is required. The environment is intentionally lightweight and only installs two packages: `aggdraw` and `pillow`.

## Usage

```bash
./run.sh
```

After running it, enter the size in px.

Examples:

- Enter `3000`: creates 3000x3000 PNG files with a transparent background in `out_3000/`
- Enter `500`, then `ffffff`: creates 500x500 PNG files with a white background in `out_500_ffffff/`

Output folders are named `out_[size]` or `out_[size]_[background]`.
Output files are named `[logo]_[size]_[background].png`, e.g. `psl_logo_black_500_ffffff.png`.

## GitHub Actions

You can also generate PNG files from GitHub:

1. Go to **Actions**.
2. Select **Make PNG**.
3. Click **Run workflow**.
4. Enter `size` and optionally `background`.
5. Download the generated PNG artifact after the workflow finishes.
