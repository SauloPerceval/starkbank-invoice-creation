import json
import logging
from random import randint

from clients.starkbank import Invoice, StarkBankAdapter
from config import StagingConfig
from helpers import generate_random_cpf

logger = logging.getLogger()
logger.setLevel("INFO")


def lambda_handler(event: dict, context, config=StagingConfig()):
    sb_adapter = StarkBankAdapter(config=config)

    number_of_invoices = randint(
        int(config["MIN_INVOICES_QUANTITY"]), int(config["MAX_INVOICES_QUANTITY"])
    )
    logger.info(f"Generating data for {number_of_invoices} invoices")

    invoices = [
        Invoice(
            amount=randint(0, 10000000),
            payer_cpf=generate_random_cpf(),
            payer_name="Fulano da Silva",
        )
        for _ in range(number_of_invoices)
    ]

    logger.info(f"Creating {number_of_invoices} invoices on Starkbank")
    result = sb_adapter.send_invoices(invoices=invoices)

    logger.info(f"Created invoices ids: {result}")
