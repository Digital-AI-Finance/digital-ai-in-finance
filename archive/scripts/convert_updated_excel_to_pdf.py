import os
import win32com.client as win32
from pathlib import Path

def excel_to_pdf_optimized(excel_path, pdf_path):
    """
    Convert Excel file to PDF with optimized layout for fewer pages
    """
    # Get absolute paths
    excel_path = os.path.abspath(excel_path)
    pdf_path = os.path.abspath(pdf_path)

    # Check if Excel file exists
    if not os.path.exists(excel_path):
        print(f"Error: Excel file not found: {excel_path}")
        return False

    try:
        # Initialize Excel application
        excel = win32.Dispatch('Excel.Application')
        excel.Visible = False
        excel.DisplayAlerts = False

        # Open the workbook
        workbook = excel.Workbooks.Open(excel_path)

        # Process each worksheet with optimized settings
        sheet_settings = {
            "Gantt Chart": {
                "zoom": 65,  # Zoom to fit 8-month timeline better
                "fit_wide": 1,
                "fit_tall": 2,
                "print_area": "A1:N55"  # Adjusted for 8 months
            },
            "Resource Summary": {
                "zoom": 100,
                "fit_wide": 1,
                "fit_tall": 1,
                "print_area": "A1:C10"
            },
            "Milestones": {
                "zoom": 100,
                "fit_wide": 1,
                "fit_tall": 1,
                "print_area": "A1:C9"  # One less milestone now
            },
            "Timeline Summary": {
                "zoom": 100,
                "fit_wide": 1,
                "fit_tall": 1,
                "print_area": "A1:C7"
            }
        }

        for sheet in workbook.Worksheets:
            settings = sheet_settings.get(sheet.Name, {})

            # Set to landscape orientation
            sheet.PageSetup.Orientation = 2  # xlLandscape

            # Set zoom if specified
            if "zoom" in settings:
                sheet.PageSetup.Zoom = settings["zoom"]
            else:
                sheet.PageSetup.Zoom = False

            # Set print area if specified
            if "print_area" in settings:
                sheet.PageSetup.PrintArea = settings["print_area"]

            # Fit to pages settings
            if sheet.PageSetup.Zoom == False:
                sheet.PageSetup.FitToPagesWide = settings.get("fit_wide", 1)
                sheet.PageSetup.FitToPagesTall = settings.get("fit_tall", 1)

            # Minimal margins (in points)
            sheet.PageSetup.LeftMargin = 18
            sheet.PageSetup.RightMargin = 18
            sheet.PageSetup.TopMargin = 18
            sheet.PageSetup.BottomMargin = 18
            sheet.PageSetup.HeaderMargin = 9
            sheet.PageSetup.FooterMargin = 9

            # Center on page
            sheet.PageSetup.CenterHorizontally = True
            sheet.PageSetup.CenterVertically = False

            # Compact header and footer
            sheet.PageSetup.CenterHeader = f"&8{sheet.Name}"
            sheet.PageSetup.CenterFooter = "&8Page &P"

            # Print quality
            sheet.PageSetup.Draft = False
            sheet.PageSetup.PrintQuality = 600

        # Select all sheets to export as single PDF
        workbook.Worksheets.Select()

        # Export as PDF
        workbook.ExportAsFixedFormat(
            Type=0,
            Filename=pdf_path,
            Quality=0,
            IncludeDocProperties=True,
            IgnorePrintAreas=False,
            OpenAfterPublish=False
        )

        # Close workbook and quit Excel
        workbook.Close(SaveChanges=False)
        excel.Quit()

        print(f"Successfully converted to optimized PDF: {pdf_path}")
        return True

    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        try:
            excel.Quit()
        except:
            pass
        return False

def create_single_page_gantt_pdf(excel_path, pdf_path):
    """
    Create a single-page version focusing on the main Gantt chart
    """
    try:
        excel = win32.Dispatch('Excel.Application')
        excel.Visible = False
        excel.DisplayAlerts = False

        workbook = excel.Workbooks.Open(os.path.abspath(excel_path))

        # Focus only on the main Gantt Chart sheet
        gantt_sheet = workbook.Worksheets("Gantt Chart")

        # Ultra-compact settings for single page
        gantt_sheet.PageSetup.Orientation = 2  # Landscape
        gantt_sheet.PageSetup.Zoom = 45  # Smaller zoom for 8-month timeline

        # Minimal margins
        gantt_sheet.PageSetup.LeftMargin = 10
        gantt_sheet.PageSetup.RightMargin = 10
        gantt_sheet.PageSetup.TopMargin = 10
        gantt_sheet.PageSetup.BottomMargin = 10
        gantt_sheet.PageSetup.HeaderMargin = 5
        gantt_sheet.PageSetup.FooterMargin = 5

        # Simple header
        gantt_sheet.PageSetup.CenterHeader = "CCG Workshop Gantt Chart (Dec 2025 - Jul 2026)"
        gantt_sheet.PageSetup.CenterFooter = ""

        # Export just this sheet
        gantt_sheet.ExportAsFixedFormat(0, os.path.abspath(pdf_path))

        workbook.Close(SaveChanges=False)
        excel.Quit()

        print(f"Single-page Gantt PDF created: {pdf_path}")
        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        try:
            excel.Quit()
        except:
            pass
        return False

if __name__ == "__main__":
    excel_file = r"D:\Joerg\Research\slides\2025_LeadingHouse_Travel\20241031_CCG_Workshop_Gantt_Chart_Updated.xlsx"

    # Create optimized multi-page version
    pdf_optimized = r"D:\Joerg\Research\slides\2025_LeadingHouse_Travel\20241031_CCG_Gantt_Updated_Optimized.pdf"
    excel_to_pdf_optimized(excel_file, pdf_optimized)

    # Create ultra-compact single page version
    pdf_single = r"D:\Joerg\Research\slides\2025_LeadingHouse_Travel\20241031_CCG_Gantt_Updated_SinglePage.pdf"
    create_single_page_gantt_pdf(excel_file, pdf_single)

    print("\nCreated two PDF versions of the UPDATED timeline:")
    print("1. Optimized version: 20241031_CCG_Gantt_Updated_Optimized.pdf")
    print("2. Single-page version: 20241031_CCG_Gantt_Updated_SinglePage.pdf")