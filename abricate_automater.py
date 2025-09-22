#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
import glob

import re

def get_accession(fasta_file):
    """Extract accession from FASTA header."""
    try:
        with open(fasta_file, 'r') as f:
            line = f.readline().strip()
            if line.startswith('>'):
                header_content = line[1:].strip()
                if header_content:
                    potential_accession = header_content.split()[0]
                    if potential_accession and is_valid_accession(potential_accession):
                        return potential_accession
                # If header is empty or invalid accession, fall back to filename
                return os.path.splitext(os.path.basename(fasta_file))[0]
            else:
                # No header line, use filename
                return os.path.splitext(os.path.basename(fasta_file))[0]
    except Exception as e:
        print(f"Error parsing {fasta_file}: {e}")
        return os.path.splitext(os.path.basename(fasta_file))[0]

def is_valid_accession(accession):
    """Check if the string looks like a valid NCBI accession."""
    # Pattern: 2-4 letters, underscore, alphanumeric, optional version (.number)
    pattern = r'^[A-Z]{2,4}_[A-Z0-9]+(\.[0-9]+)?$'
    return bool(re.match(pattern, accession))

def find_abricate_path():
    """Find the full path to abricate executable."""
    # Try common locations
    possible_paths = [
        'abricate',  # In PATH
        os.path.join(os.getcwd(), 'abricate.cmd'),  # Local mock for testing
        '/usr/local/bin/abricate',  # System install
        os.path.expanduser('~/miniconda3/bin/abricate'),  # Miniconda
        os.path.expanduser('~/miniconda3/envs/abricate-env/bin/abricate'),  # Conda env
        os.path.expanduser('~/anaconda3/bin/abricate'),  # Anaconda
    ]

    for path in possible_paths:
        try:
            result = subprocess.run([path, '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return path
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            continue

    return None

def run_abricate(fasta_file, output_file, db='card'):
    """Run ABRicate on a FASTA file."""
    abricate_path = find_abricate_path()
    if not abricate_path:
        print("ABRicate not found. Please install ABRicate and ensure it's in PATH.")
        return False

    cmd = [abricate_path, '--db', db, fasta_file]

    try:
        with open(output_file, 'w') as out:
            result = subprocess.run(cmd, stdout=out, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"ABRicate failed for {fasta_file}: {result.stderr.strip()}")
            return False
        return True
    except Exception as e:
        print(f"Error running ABRicate on {fasta_file}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Automate ABRicate runs on multiple genome FASTA files against CARD database.')
    parser.add_argument('--input-dir', required=True, help='Directory containing FASTA files')
    parser.add_argument('--output-dir', required=True, help='Directory to save .tsv output files')
    parser.add_argument('--db', default='card', help='ABRicate database (default: card)')
    parser.add_argument('--skip-check', action='store_true', help='Skip ABRicate installation check (for testing)')
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    db = args.db
    skip_check = args.skip_check

    # Check if input dir exists
    if not os.path.isdir(input_dir):
        print(f"Input directory {input_dir} does not exist.")
        sys.exit(1)

    # Create output dir if not exists
    os.makedirs(output_dir, exist_ok=True)

    # Check ABRicate
    if not skip_check:
        abricate_path = find_abricate_path()
        if not abricate_path:
            print("ABRicate not found. Install via: conda install -c bioconda abricate")
            sys.exit(1)
        try:
            result = subprocess.run([abricate_path, '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                print("ABRicate not properly installed.")
                sys.exit(1)
        except subprocess.TimeoutExpired:
            print("ABRicate check timed out.")
            sys.exit(1)
        except Exception as e:
            print(f"Error checking ABRicate: {e}")
            sys.exit(1)

    # Find FASTA files
    fasta_files = glob.glob(os.path.join(input_dir, '*.fasta')) + \
                  glob.glob(os.path.join(input_dir, '*.fa')) + \
                  glob.glob(os.path.join(input_dir, '*.fna'))

    if not fasta_files:
        print(f"No FASTA files found in {input_dir}")
        sys.exit(1)

    print(f"Found {len(fasta_files)} FASTA files.")

    processed = 0
    for fasta_file in fasta_files:
        accession = get_accession(fasta_file)
        output_file = os.path.join(output_dir, f"{accession}.tsv")
        print(f"Processing {os.path.basename(fasta_file)} -> {accession}.tsv")
        if run_abricate(fasta_file, output_file, db):
            processed += 1
        else:
            print(f"Failed to process {fasta_file}")

    print(f"Successfully processed {processed}/{len(fasta_files)} files.")

if __name__ == '__main__':
    main()