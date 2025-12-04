# ABRicate Automater

A Python script to automate running ABRicate on multiple genome FASTA files against the CARD database for antimicrobial resistance gene detection.

## Features

- Processes multiple FASTA files in a directory
- Extracts genome accession from FASTA headers
- Runs ABRicate with any database on ABRicate (preferably with CARD)
- Outputs .tsv files named after genome accessions
- Handles errors gracefully and continues processing

## 🚀 **Complete Setup Guide**

### **Why This Setup Process?**

ABRicate requires:
- **BLAST+ database engine** for sequence alignment
- **CARD database** (Comprehensive Antibiotic Resistance Database) with 2,600+ resistance genes
- **Proper environment isolation** to avoid dependency conflicts

The setup ensures you have all components working together seamlessly.

### **Quick Start (One-Command Setup)**

**For first-time users**, simply run:
```bash
python abricate_automater.py --auto-setup --input-dir your/genomes --output-dir results
```

This will automatically:
- ✅ Install Miniconda (if needed)
- ✅ Create isolated ABRicate environment
- ✅ Install ABRicate with CARD database
- ✅ Run your analysis

### **Manual Installation (Advanced Users)**

#### **Option 1: Automated Setup Script**
```bash
python setup.py
```
*Recommended for most users - handles all dependencies automatically*

#### **Option 2: Conda (Linux/Mac)**
```bash
# Install conda environment
conda create -n abricate-env -c bioconda abricate -y
conda activate abricate-env

# Setup CARD database
abricate --setupdb
```

#### **Option 3: WSL (Windows)**
```bash
# In WSL terminal
sudo apt update
sudo apt install abricate

# Setup CARD database
abricate --setupdb
```

### **Post-Installation Verification**

1. **Check ABRicate installation**:
   ```bash
   abricate --version
   # Should show version info
   ```

2. **Verify CARD database**:
   ```bash
   abricate --list
   # Should show: card  Comprehensive Antibiotic Resistance Database
   ```

3. **Test with sample genome**:
   ```bash
   abricate --db card your_genome.fasta | head -5
   # Should show TSV headers and gene detections
   ```

### **Usage Instructions**

#### **Basic Usage**
```bash
python abricate_automater.py --input-dir input/ --output-dir results/
```

#### **Advanced Options**
```bash
# Use different database
python abricate_automator.py --input-dir input/ --output-dir results/ --db ncbi

# Skip ABRicate checks (for testing)
python abricate_automator.py --input-dir input/ --output-dir results/ --skip-check
```

### **Output Files**

Each genome generates a `.tsv` file with:
- **Gene coordinates** (START/END positions)
- **Resistance categories** (aminoglycoside, beta-lactam, etc.)
- **Coverage percentages** and identity scores
- **CARD database annotations** and references

### **Troubleshooting**

**"ABRicate not found"**:
- Run setup: `python setup.py`
- Or activate environment: `conda activate abricate-env`

**"BLAST database not found"**:
- Run: `abricate --setupdb`

**Permission errors**:
- On Windows: Run terminal as administrator
- On Linux/Mac: May need `sudo` for system installation

**Requirements**: Python 3.6+, internet connection for setup

## Usage

```bash
python abricate_automator.py --input-dir /path/to/fasta/files --output-dir /path/to/output
```

**Note for Windows users**: If paths contain spaces, enclose them in quotes:
```bash
python abricate_automator.py --input-dir "C:\Path With Spaces\input" --output-dir "C:\Path With Spaces\output"
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
