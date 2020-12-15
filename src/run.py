import json
import optparse
import os

from deanonymize_html import DeanonymizeHTML
from utils_report import UtilsReport


def deanonymize_report(
    report, data, layout, output_dir, delimiter, batch_text
):
    """Deanonymize report and convert it to PDF."""
    output_filename = DeanonymizeHTML.replace_html(
        report, data, delimiter, batch_text
    )
    with open(layout) as json_file:
        UtilsReport.write_pdf_landscape(
            output_filename, json.load(json_file), output_dir
        )
    os.remove(output_filename)


if __name__ == "__main__":

    parser = optparse.OptionParser()

    parser.add_option(
        "-d", "--data", dest="data", help="Deanonymized data filename"
    )
    parser.add_option("-l", "--layout", dest="layout", help="PDF layout")
    parser.add_option(
        "-r", "--report", dest="report", help="Report file or directory name"
    )
    parser.add_option("-o", "--output", dest="output", help="Output directory")
    parser.add_option(
        "--delimiter",
        dest="delimiter",
        default=",",
        help="delimiter in the data filename, default value ',' ",
    )
    parser.add_option(
        "--batch-month",
        dest="batch_month",
        help="Batch month to be included in the filename",
    )
    parser.add_option(
        "--batch-number",
        dest="batch_number",
        help="Batch number to be included in the filename",
    )

    (options, args) = parser.parse_args()

    if not os.path.exists(options.output):
        print("Output directory %s created" % options.output)
        os.mkdir(options.output)

    if os.path.isdir(options.report):
        onlyfiles = [
            f
            for f in os.listdir(options.report)
            if os.path.isfile(os.path.join(options.report, f))
        ]
        for report in onlyfiles:
            deanonymize_report(
                os.path.join(options.report, report),
                options.data,
                options.layout,
                options.output,
                options.delimiter,
                str(options.batch_month) + "-" + str(options.batch_number),
            )

    if os.path.isfile(options.report):
        deanonymize_report(
            options.report,
            options.data,
            options.layout,
            options.output,
            options.delimiter,
            str(options.batch_month) + "-" + str(options.batch_number),
        )
