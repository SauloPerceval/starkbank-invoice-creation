from unittest import mock

import starkbank
from clients.starkbank import Invoice, StarkBankAdapter


@mock.patch.object(starkbank.invoice, "create")
class TestStarkBankAdapterSendInvoices:
    def test_successes(self, sb_invoice_create_mock, testing_config):
        sb_adapter = StarkBankAdapter(config=testing_config)
        invoices = [
            Invoice(amount=10000, payer_cpf="00536382719", payer_name="John Doe"),
            Invoice(amount=20000, payer_cpf="55371035400", payer_name="Jane Doe"),
        ]
        sb_invoice_create_mock.return_value = [
            starkbank.Invoice(
                amount=10000,
                tax_id="00536382719",
                name="John Doe",
                tags=["test"],
                id=1,
            ),
            starkbank.Invoice(
                amount=20000,
                tax_id="55371035400",
                name="Jane Doe",
                tags=["test"],
                id=2,
            ),
        ]

        result = sb_adapter.send_invoices(invoices=invoices, tag="test")

        assert result == ["1", "2"]
        for sent_invoice, invoice in zip(
            sb_invoice_create_mock.call_args.args[0], invoices
        ):
            assert sent_invoice.amount == invoice.amount
            assert sent_invoice.tax_id == invoice.payer_cpf
            assert sent_invoice.name == invoice.payer_name
            assert sent_invoice.tags == ["test"]
