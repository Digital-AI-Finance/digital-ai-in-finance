import os
import win32com.client as win32
from pathlib import Path

def excel_to_pdf_optimized(excel_path, pdf_path):
    """
    Convert Excel file to PDF with optimized layout for fewer pages
    Using 16:9 aspect ratio and better page setup
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
        excel.Visible = False  # Don't show Excel window
        excel.DisplayAlerts = False  # Don't show alerts

        # Open the workbook
        workbook = excel.Workbooks.Open(excel_path)

        # Process each worksheet with optimized settings
        sheet_settings = {
            "Gantt Chart": {
                "zoom": 60,  # Zoom out to fit more content
                "fit_wide": 1,  # Fit to 1 page wide
                "fit_tall": 2,  # Allow up to 2 pages tall for Gantt
                "print_area": "A1:AG60"  # Adjust based on content
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
                "print_area": "A1:C10"
            }
        }

        for sheet in workbook.Worksheets:
            settings = sheet_settings.get(sheet.Name, {})

            # Set to landscape orientation for 16:9 aspect
            sheet.PageSetup.Orientation = 2  # xlLandscape

            # Set paper size to A3 for more space (or custom)
            # sheet.PageSetup.PaperSize = 8  # xlPaperA3

            # Set zoom if specified
            if "zoom" in settings:
                sheet.PageSetup.Zoom = settings["zoom"]
            else:
                sheet.PageSetup.Zoom = False  # Use fit to page instead

            # Set print area if specified
            if "print_area" in settings:
                sheet.PageSetup.PrintArea = settings["print_area"]

            # Fit to pages settings
            if sheet.PageSetup.Zoom == False:
                sheet.PageSetup.FitToPagesWide = settings.get("fit_wide", 1)
                sheet.PageSetup.FitToPagesTall = settings.get("fit_tall", 1)

            # Minimize margins for maximum content (in points)
            sheet.PageSetup.LeftMargin = 18  # 0.25 inch
            sheet.PageSetup.RightMargin = 18
            sheet.PageSetup.TopMargin = 18
            sheet.PageSetup.BottomMargin = 18
            sheet.PageSetup.HeaderMargin = 9
            sheet.PageSetup.FooterMargin = 9

            # Center on page
            sheet.PageSetup.CenterHorizontally = True
            sheet.PageSetup.CenterVertically = False

            # Compact header and footer
            sheet.PageSetup.LeftHeader = ""
            sheet.PageSetup.CenterHeader = f"&8{sheet.Name}"  # Smaller font
            sheet.PageSetup.RightHeader = ""
            sheet.PageSetup.LeftFooter = ""
            sheet.PageSetup.CenterFooter = "&8Page &P"  # Smaller font
            sheet.PageSetup.RightFooter = ""

            # Print quality
            sheet.PageSetup.Draft = False
            sheet.PageSetup.PrintQuality = 600  # Higher quality

        # Select all sheets to export as single PDF
        workbook.Worksheets.Select()

        # Export as PDF (0 = xlTypePDF)
        workbook.ExportAsFixedFormat(
            Type=0,  # PDF
            Filename=pdf_path,
            Quality=0,  # xlQualityStandard (0) or xlQualityMinimum (1)
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
    Alternative: Create a more compact single-page version focusing on the main Gantt chart
    """
    try:
        excel = win32.Dispatch('Excel.Application')
        excel.Visible = False
        excel.DisplayAlerts = False

        workbook = excel.Workbooks.Open(os.path.abspath(excel_path))

        # Focus only on the main Gantt Chart sheet
        gantt_sheet = workbook.Worksheets("Gantt Chart")

        # Hide less critical rows/columns if needed
        # gantt_sheet.Columns("G:G").Hidden = True  # Hide Resources column if needed

        # Ultra-compact settings for single page
        gantt_sheet.PageSetup.Orientation = 2  # Landscape
        gantt_sheet.PageSetup.Zoom = 40  # Very small zoom to fit everything

        # Minimal margins
        gantt_sheet.PageSetup.LeftMargin = 10
        gantt_sheet.PageSetup.RightMargin = 10
        gantt_sheet.PageSetup.TopMargin = 10
        gantt_sheet.PageSetup.BottomMargin = 10
        gantt_sheet.PageSetup.HeaderMargin = 5
        gantt_sheet.PageSetup.FooterMargin = 5

        # Remove headers/footers for more space
        gantt_sheet.PageSetup.LeftHeader = ""
        gantt_sheet.PageSetup.CenterHeader = "CCG Workshop Gantt Chart (Apr 2026)"
        gantt_sheet.PageSetup.RightHeader = ""
        gantt_sheet.PageSetup.LeftFooter = ""
        gantt_sheet.PageSetup.CenterFooter = ""
        gantt_sheet.PageSetup.RightFooter = ""

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
    excel_file = r"D:\Joerg\Research\slides\2025_LeadingHouse_Travel\20241031_CCG_Workshop_Gantt_Chart.xlsx"

    # Create optimized multi-page version (fewer pages)
    pdf_optimized = r"D:\Joerg\Research\slides\2025_LeadingHouse_Travel\20241031_CCG_Workshop_Gantt_Chart_Optimized.pdf"
    excel_to_pdf_optimized(excel_file, pdf_optimized)

    # Create ultra-compact single page version
    pdf_single = r"D:\Joerg\Research\slides\2025_LeadingHouse_Travel\20241031_CCG_Workshop_Gantt_Chart_SinglePage.pdf"
    create_single_page_gantt_pdf(excel_file, pdf_single)

    print("\nCreated two PDF versions:")
    print("1. Optimized version (fewer pages): 20241031_CCG_Workshop_Gantt_Chart_Optimized.pdf")
    print("2. Single-page version (compact): 20241031_CCG_Workshop_Gantt_Chart_SinglePage.pdf")