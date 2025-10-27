#!/usr/bin/env python3
from bibbrowser.config import Config
import bibbrowser.version 
# from doi2bib import crossref

CLIPBOARDCOPYCOMMAND = Config.get('executables','ClipBoardCopyCommand')
OPENCOMMAND = Config.get('executables','OpenFileCommand')
EDITOR = Config.get('executables','Editor')
DATABASE = Config.get("files","database")
SLEEPTIME = float(Config.get("others","sleeptime"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bibbrowser.config import Config

import sys
import os
import re
from sqlalchemy import text
import signal
import pybtex
from bibbrowser.pybtex_interface import pybtex_to_bibbrowser
from bibbrowser.attach_file import attach_file
import subprocess

from bibbrowser.table_def import Entry, Author, Identity, Search, Field, Editor

import subprocess
import xml.etree.ElementTree as ET

# open the database
engine = create_engine('sqlite:///'+DATABASE, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Path to your .bcf file
bcf_file = "lphys1213.bcf"
output_file = "bibtex.bib"

# Parse the .bcf XML file
tree = ET.parse(bcf_file)
root = tree.getroot()

# Extract namespace
ns = {'bcf': 'https://sourceforge.net/projects/biblatex'}


# Extract unique citation keys in order
citations = []
seen = set()
for cite in root.findall(".//bcf:section/bcf:citekey", ns):
    if cite.text:
        key = cite.text.strip()
        if key not in seen:
            citations.append(key)
            seen.add(key)

print(f"Found {len(citations)} citations: {citations}")

# Generate BibTeX for each key and write to output
with open(output_file, "w") as f:
    for key in citations:
        entries = session.query(Entry).filter(Entry.entry_key == key).all()
        if not entries:
            print(f"Warning: no entry found in DB for {key}")
            continue
        for entry in entries:
            try:
                bibtex_entry = entry.generate_bibtex()
                f.write(bibtex_entry)
                f.write("\n\n")
                print(f"Wrote BibTeX for {key}")
            except Exception as e:
                print(f"Warning: failed to generate BibTeX for {key}: {e}")

