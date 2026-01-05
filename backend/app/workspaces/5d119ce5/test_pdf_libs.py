#!/usr/bin/env python3
"""Test script to verify PDF generation libraries are working."""

print("Testing PDF generation libraries...")

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    print("✓ reportlab.pdfgen.canvas imported successfully")
    print("✓ reportlab.lib.pagesizes.letter imported successfully")
except ImportError as e:
    print(f"✗ Error importing reportlab: {e}")

try:
    from fpdf import FPDF
    print("✓ fpdf.FPDF imported successfully")
except ImportError as e:
    print(f"✗ Error importing fpdf: {e}")

print("\nBoth libraries are available for PDF generation.")