# PSL PNG Logo

It converts the SVG logos in the `svg/` folder into square PNG logos.

## GitHub Actions

Generate PNG files directly from GitHub:

1. Go to **Actions**.
2. Select **Make PNG**.
3. Click **Run workflow**.
4. Enter `size`.
5. Leave `background` empty for transparent, or enter a hex color like `ffffff`.
6. Download the generated PNG artifact after the workflow finishes.

Examples:

- `size`: `3000`, `background`: empty creates 3000x3000 PNG files with a transparent background in `out_3000/`
- `size`: `500`, `background`: `ffffff` creates 500x500 PNG files with a white background in `out_500_ffffff/`

Output folders are named `out_[size]` or `out_[size]_[background]`.
Output files are named `[logo]_[size]_[background].png`, e.g. `psl_logo_black_500_ffffff.png`.

## Local Usage

Run:

```bash
./run.sh
```

After running it, enter the size in px.

Examples:

- Enter `3000`: creates 3000x3000 PNG files with a transparent background in `out_3000/`
- Enter `500`, then `ffffff`: creates 500x500 PNG files with a white background in `out_500_ffffff/`

`run.sh` automatically creates `.venv` and installs the required packages. Python 3 is required. The environment only installs `aggdraw` and `pillow`.
