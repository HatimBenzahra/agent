#!/usr/bin/env python3
import sys

def check_reportlab():
    try:
        import reportlab
        print("reportlab is installed")
        print(f"Version: {reportlab.__version__}")
        return True
    except ImportError:
        print("reportlab is NOT installed")
        return False

if __name__ == "__main__":
    if check_reportlab():
        sys.exit(0)
    else:
        sys.exit(1)