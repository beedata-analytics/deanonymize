import itertools
import json
import os
from multiprocessing import Pool

import click
from tqdm import tqdm

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
    "--output", type=click.Path(exists=True), help="Output directory",
)
@click.option(
    "--delimiter",
    type=click.STRING,
    default=",",
    help="delimiter in the data filename, default value ',' ",
)
@click.option(
    "--batch-month",
    type=click.INT,
    help="Batch month to be included in the filename",
)
@click.option(
    "--batch-number",
    type=click.INT,
    help="Batch number to be included in the filename",
)
@click.option("--processes", default=2, type=click.INT)
def run(
    data,
    layout,
    report,
    output,
    delimiter,
    batch_month,
    batch_number,
    processes,
):
    if not os.path.exists(output):
        print("Output directory %s created" % output)
        os.mkdir(output)

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
                [batch_month],
                [batch_number],
            )
        )

        pool = Pool(processes=processes)
        with tqdm(total=len(docs)) as pbar:
            for result in pool.imap_unordered(func=deanonymize, iterable=docs):
                pbar.update()

        for filename in onlyfiles:
            deanonymize_report(
                filename,
                data,
                layout,
                output,
                delimiter,
                str(batch_month) + "-" + str(batch_number),
            )

    if os.path.isfile(report):
        deanonymize_report(
            report,
            data,
            layout,
            output,
            delimiter,
            str(batch_month) + "-" + str(batch_number),
        )


def deanonymize(contract):
    (
        report,
        data,
        layout,
        output,
        delimiter,
        batch_month,
        batch_number,
    ) = contract
    deanonymize_report(
        report,
        data,
        layout,
        output,
        delimiter,
        str(batch_month) + "-" + str(batch_number),
    )


if __name__ == "__main__":
    run()
