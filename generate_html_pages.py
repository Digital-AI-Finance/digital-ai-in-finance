"""
Generate HTML marketing pages for AI for Digital Finance workshop

Main output: ai_digital_finance.html (single comprehensive page)

Legacy files (archived):
- archive/html/workshop_showcase.html
- archive/html/budget_showcase.html
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent

def main():
    """Generate the comprehensive HTML page"""

    print("=" * 60)
    print("AI for Digital Finance - HTML Generator")
    print("=" * 60)

    # Run the main generator script
    generator_script = BASE_DIR / "generate_ai_digital_finance.py"

    if generator_script.exists():
        print(f"\nRunning: {generator_script.name}")
        result = subprocess.run(
            [sys.executable, str(generator_script)],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"Error: {result.stderr}")
            return 1
    else:
        print(f"Error: Generator script not found: {generator_script}")
        return 1

    # Check output
    output_file = BASE_DIR / "ai_digital_finance.html"
    if output_file.exists():
        print(f"\nOutput: {output_file}")
        print(f"Size: {output_file.stat().st_size / 1024:.1f} KB")
        print("\nDone!")
    else:
        print("Error: Output file was not created")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
