import pdfkit


class UtilsReport(object):

    @staticmethod
    def write_pdf_landscape(filename, options, output_dir='output'):
        """Converts html to a landscape pdf."""
        try:
            output = filename.replace('html', 'pdf')
            pdfkit.from_file(str(filename), str(output), options=options)
        except Exception, e:
            raise Exception('''Report in pdf for file %s was not generated
                due to problems in the write_pdf function. Error: %s''' % (filename, e))
        return output
