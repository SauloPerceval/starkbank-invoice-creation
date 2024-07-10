from unittest import mock

from clients.starkbank import Invoice, StarkBankAdapter
from lambda_function import lambda_handler


@mock.patch.object(StarkBankAdapter, "send_invoices")
class TestLambdaHandler:
    def test_success(self, send_invoices_mock, testing_config):
        send_invoices_mock.return_value = ["1"]

        lambda_handler({}, context=mock.ANY, config=testing_config)

        send_invoices_mock.assert_called_once_with(
            invoices=[
                Invoice(
                    amount=mock.ANY, payer_cpf=mock.ANY, payer_name="Fulano da Silva"
                )
            ],
            tag=testing_config["INVOICES_TAG"],
        )
