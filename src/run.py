import optparse
from utils_report import UtilsReport


if __name__ == "__main__":

    parser = optparse.OptionParser()
    parser.add_option('-c', '--contracts', dest='contracts', help='Contracts')

    (options, args) = parser.parse_args()

    UtilsReport.write_pdf_landscape('697', 201905)
