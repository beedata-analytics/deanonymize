import itertools
import json
import logging
import os
import codecs
import csv
import unicodedata
import click

from multiprocessing import Pool
from deanonymize_html import DeanonymizeHTML
from tqdm import tqdm
from utils_report import UtilsReport

logger = logging.getLogger(__name__)


def deanonymize_report(
    report, data, layout, output_dir, delimiter, id, batch_text, update
):
    """Deanonymize report and convert it to PDF."""

    target = None
    try:
        target = DeanonymizeHTML.get_filename(report, batch_text)
        pdf_filename = UtilsReport.get_output_filename(target, output_dir)
        if not os.path.exists(pdf_filename) or update:
            DeanonymizeHTML.replace_html(
                report, target, data
            )
            with open(layout) as json_file:
                UtilsReport.write_pdf_landscape(
                    target, json.load(json_file), pdf_filename
                )
    except Exception as e:
        logger.exception("Error deanonymizing report %s: %s", (id, e))

    try:
        if target is not None:
            os.remove(target)
    except OSError:
        pass


def read_data(data_file, delimiter, id):
    rows = {}
    with codecs.open(data_file, mode="r", encoding="utf-8") as infile:
        csv_reader = csv.DictReader(infile, delimiter=delimiter)
        for row in csv_reader:
            contract_key = UtilsReport.valid_variable_name(row[id])

            rows.update(
                {
                    contract_key:
                        {
                            "%s_%s"
                            % (
                                unicodedata.normalize("NFKD", cell)
                                .encode("ascii", "ignore")
                                .decode("ascii")
                                .replace(" ", "_"),
                                contract_key,
                            ): row[cell]
                            for cell in row.keys()
                        }
                }
            )

    return rows


@click.command()
@click.option(
    "--data", type=click.Path(exists=True), help="Deanonymized data filename"
)
@click.option("--layout", type=click.Path(exists=True), help="PDF layout")
@click.option(
    "--report",
    type=click.Path(exists=True),
    help="Report file or directory name",
)
@click.option(
    "--output",
    type=click.Path(exists=True),
    help="Output directory",
)
@click.option(
    "--delimiter",
    type=click.STRING,
    default=",",
    help="Delimiter in the data filename, default value ',' ",
)
@click.option(
    "--id",
    type=click.STRING,
    default="id",
    help="Identifier in the data filename",
)
@click.option(
    "--batch-month",
    type=click.STRING,
    help="Batch month to be included in the filename",
)
@click.option(
    "--batch-number",
    type=click.STRING,
    help="Batch number to be included in the filename",
)
@click.option('--update/--no-update', default=False)
@click.option("--processes", default=16, type=click.INT)
def run(
    data,
    layout,
    report,
    output,
    delimiter,
    id,
    batch_month,
    batch_number,
    processes,
    update,
):
    if not os.path.exists(output):
        print("Output directory %s created" % output)
        os.mkdir(output)


    data = read_data(data, delimiter, id)

    if os.path.isdir(report):
        onlyfiles = [
            os.path.join(report, f)
            for f in os.listdir(report)
            if os.path.isfile(os.path.join(report, f))
        ]
        docs = list(
            itertools.product(
                onlyfiles,
                [data],
                [layout],
                [output],
                [delimiter],
                [id],
                [batch_month],
                [batch_number],
                [update],
            )
        )

        if processes > 1:
            pool = Pool(processes=processes)
            with tqdm(total=len(docs)) as pbar:
                for result in pool.imap_unordered(
                    func=deanonymize, iterable=docs
                ):
                    pbar.update()
        else:
            with tqdm(total=len(docs)) as pbar:
                for doc in docs:
                    deanonymize(doc)
                    pbar.update()

    if os.path.isfile(report):
        deanonymize_report(
            report,
            data,
            layout,
            output,
            delimiter,
            id,
            str(batch_month) + "-" + str(batch_number),
            update,
        )


def deanonymize(contract):
    (
        report,
        data,
        layout,
        output,
        delimiter,
        id,
        batch_month,
        batch_number,
        update,
    ) = contract
    deanonymize_report(
        report,
        data,
        layout,
        output,
        delimiter,
        id,
        "%s%s" % (str(batch_month), ("-" + str(batch_number)) if batch_number is not None else ""),
        update,
    )

if __name__ == "__main__":
    run()
