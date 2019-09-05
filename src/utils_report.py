import pdfkit


class UtilsReport(object):

    @staticmethod
    def write_pdf_landscape(contract_name, period, javascript_delay=0, output_dir='output'):
        try:
            options = {
                "--margin-left": "0",  # default is 10 = 14 mm
                "--margin-right": "10",  # default is 10
                "--margin-top": "10",  # default is 10  42.9
                "--margin-bottom": "0",
                "--page-size": "A4",
                "--orientation": "Landscape",
                "--zoom": "2",
                "--javascript-delay": str(javascript_delay)
            }

            input = "output/%s~%s.html" % (contract_name, period)
            output = "%s/%s~%s.pdf" % (output_dir, contract_name, period)

            pdfkit.from_file(str(input), str(output), options=options)
        except Exception, e:
            raise Exception('''Report in pdf for contractId %s was not generated due to problems
                in the write_pdf function. Error: %s''' % (contract_name, e))
