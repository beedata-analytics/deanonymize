import pdfkit
from os import path


class UtilsReport(object):
    @staticmethod
    def write_pdf_landscape(filename, options, output_dir):
        """Converts html to a landscape pdf."""
        try:
            output = path.join(output_dir, path.basename(filename)).replace(
                "html", "pdf"
            )
            pdfkit.from_file(str(filename), str(output), options=options)
        except Exception as e:
            raise Exception(
                "Report in pdf for file %s was not generated due to problems "
                "in the write_pdf function. Error: %s" % (filename, e)
            )
        return output
