import optparse
import json

from utils_report import UtilsReport
from deanonymize_html import DeanonymizeHTML


if __name__ == "__main__":

    parser = optparse.OptionParser()

    parser.add_option('-d', '--data', dest='data', help='Deanonymized data filename')
    parser.add_option('-l', '--layout', dest='layout', help='PDF layout')
    parser.add_option('-r', '--report', dest='report', help='Report filename')

    (options, args) = parser.parse_args()

    # Deanonymize report
    output_filename = DeanonymizeHTML.replace_html(options.report, options.data)

    # Generate PDF
    with open(options.layout) as json_file:
        UtilsReport.write_pdf_landscape(output_filename, json.load(json_file))
