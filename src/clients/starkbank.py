from typing import Iterable, List, NamedTuple

from config import Config


class Invoice(NamedTuple):
    amount: int
    payer_cpf: str
    payer_name: str


class StarkBankAdapter:
    def __init__(self, config: Config):
        import starkbank

        user = starkbank.Project(
            environment=config["STARKBANK_ENVIRONMENT"],
            id=config["STARKBANK_PROJECT_ID"],
            private_key=config["STARKBANK_PRIVATE_KEY_CONTENT"],
        )
        starkbank.user = user

        self._starkbank_client = starkbank
        self._invoices_tag = config["INVOICES_TAG"]

    def send_invoices(self, invoices: Iterable[Invoice]) -> List[str]:
        result_invoices = self._starkbank_client.invoice.create(
            [
                self._starkbank_client.Invoice(
                    amount=i.amount,
                    tax_id=i.payer_cpf,
                    name=i.payer_name,
                    tags=[self._invoices_tag] if self._invoices_tag else None,
                )
                for i in invoices
            ]
        )
        return [i.id for i in result_invoices]
