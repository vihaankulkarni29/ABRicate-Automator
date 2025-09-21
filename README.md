# ABRicate Automater

A Python script to automate running ABRicate on multiple genome FASTA files against the CARD database for antimicrobial resistance gene detection.

## Features

- Processes multiple FASTA files in a directory
- Extracts genome accession from FASTA headers
- Runs ABRicate with CARD database
- Outputs .tsv files named after genome accessions
- Handles errors gracefully and continues processing

## Installation

### Option 1: Conda (Recommended for Linux/Mac)
```bash
conda install -c bioconda abricate
abricate --setupdb
```

### Option 2: On Windows with WSL
If conda installation fails on Windows:
```bash
# In WSL terminal
sudo apt update
sudo apt install abricate
abricate --setupdb
```

### Option 3: Manual Installation
Follow the [ABRicate GitHub](https://github.com/tseemann/abricate) for manual installation.

Ensure Python 3.6+ is installed.

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