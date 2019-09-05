import optparse
import json

from utils_report import UtilsReport
from deanonymize_html import DeanonymizeHTML


if __name__ == "__main__":

    parser = optparse.OptionParser()
    parser.add_option('-r', '--report', dest='report', help='Report filename')

    (options, args) = parser.parse_args()

    # Deanonymize
    output_filename = DeanonymizeHTML.replace_html(options.report, 'data/data.csv')

    # Convert to PDF
    with open('config/A4-landscape.json') as json_file:
        UtilsReport.write_pdf_landscape(output_filename, json.load(json_file))
