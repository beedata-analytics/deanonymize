from os import path

import pdfkit


class UtilsReport(object):

    @staticmethod
    def get_output_filename(filename, output_dir):
        """
        Returns the output filename for the report.

        :param filename: The filename of the report.
        :param output_dir: The output directory.
        """
        return path.join(output_dir, path.basename(filename)).replace(
            "html", "pdf"
        )

    @staticmethod
    def write_pdf_landscape(filename, options, output):
        """Converts html to a landscape pdf."""
        try:
            pdfkit.from_file(str(filename), str(output), options=options)
        except Exception as e:
            raise Exception(
                "Report in pdf for file %s was not generated due to problems "
                "in the write_pdf function. Error: %s" % (filename, e)
            )
