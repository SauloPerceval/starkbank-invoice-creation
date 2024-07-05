from unittest import mock

import starkbank
from src.clients.starkbank import Invoice, StarkBankAdapter


@mock.patch.object(starkbank.invoice, "create")
def test_send_invoices(sb_invoice_create_mock, testing_config):
    sb_adapter = StarkBankAdapter(config=testing_config)
    invoices = [
        Invoice(amount=10000, payer_cpf="00536382719", payer_name="John Doe"),
        Invoice(amount=20000, payer_cpf="55371035400", payer_name="Jane Doe"),
    ]

    sb_adapter.send_invoices(invoices=invoices)

    for sent_invoice, invoice in zip(
        sb_invoice_create_mock.call_args.args[0], invoices
    ):
        assert sent_invoice.amount == invoice.amount
        assert sent_invoice.tax_id == invoice.payer_cpf
        assert sent_invoice.name == invoice.payer_name
        assert sent_invoice.tags == ["test"]
