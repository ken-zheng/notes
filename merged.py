#!/usr/bin/env python3
import os
import argparse
from pikepdf import Pdf


def main(args):
  opdf = Pdf.open(args.odd)
  epdf = Pdf.open(args.even)
  mpdf = Pdf.new()
  
  for i, page in enumerate(opdf.pages):
    mpdf.pages.append(page)
    mpdf.pages.append(epdf.pages[-(i+1)])
 
  mpdf.save(args.merged)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Canon MF634C double-sided scan processing')
  parser.add_argument('-m', '--merged', required=True, help="output merged filename") 
  parser.add_argument('-o', '--odd', required=True, help="odd number pages filename")
  parser.add_argument('-e', '--even', required=True, help="even number pages filename")
  args = parser.parse_args()
  main(args)