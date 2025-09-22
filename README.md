# ABRicate Automater

A Python script to automate running ABRicate on multiple genome FASTA files against the CARD database for antimicrobial resistance gene detection.

## Features

- Processes multiple FASTA files in a directory
- Extracts genome accession from FASTA headers
- Runs ABRicate with CARD database
- Outputs .tsv files named after genome accessions
- Handles errors gracefully and continues processing

## Quick Start (One-Command Setup)

**For first-time users**, simply run:
```bash
python abricate_automater.py --auto-setup --input-dir your/genomes --output-dir results
```

This will automatically:
- ✅ Install Miniconda (if needed)
- ✅ Create ABRicate environment
- ✅ Install ABRicate with CARD database
- ✅ Run your analysis

## Manual Installation (Advanced Users)

### Option 1: Automated Setup
```bash
python setup.py
```

### Option 2: Conda (Linux/Mac)
```bash
conda install -c bioconda abricate
abricate --setupdb
```

### Option 3: WSL (Windows)
```bash
sudo apt update && sudo apt install abricate
abricate --setupdb
```

**Requirements**: Python 3.6+

## Usage

```bash
python abricate_automater.py --input-dir /path/to/fasta/files --output-dir /path/to/output
```

**Note for Windows users**: If paths contain spaces, enclose them in quotes:
```bash
python abricate_automater.py --input-dir "C:\Path With Spaces\input" --output-dir "C:\Path With Spaces\output"
```

### Arguments

- `--input-dir`: Directory containing FASTA files (.fasta, .fa, .fna)
- `--output-dir`: Directory to save output .tsv files
- `--db`: ABRicate database (default: card)

### Example

```bash
python abricate_automater.py --input-dir genomes/ --output-dir results/
```

This will process all FASTA files in `genomes/` and save results like `NC_12345.tsv` in `results/`.

## Output

Each .tsv file contains ABRicate output with columns:
- SEQUENCE
- START
- END
- GENE
- COVERAGE
- etc.

## Requirements

- ABRicate
- CARD database
- Python 3.6+