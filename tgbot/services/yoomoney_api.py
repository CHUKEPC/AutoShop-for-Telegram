from yoomoney import Quickpay, Client


class YooMoney:
    def __init__(self, token, number):

        self.token = token
        self.number = number
        self.client = Client(self.token)

    def create_yoomoney_link(self, amount, comment):
        """
        Генерация ссылки на оплату
    
        :param amount: стоимость
        :param comment: комментарий
        :return:
        """
        payment_form = dict()

        number = self.number

        quick_pay = Quickpay(
            receiver=number,
            quickpay_form="shop",
            targets="Пополнение баланса",
            paymentType="SB",
            sum=amount,
            label=comment
        )

        payment_form["link"] = quick_pay.base_url
        payment_form['comment'] = quick_pay.label
        payment_form["key"] = "Номер"
        payment_form["value"] = number

        return payment_form

    def check_yoomoney_payment(self, comment):
        """
        Проверка оплаты

        :param comment: комментарий
        :return: true - оплата прошла, false - оплаты нет
        """

        history = self.client.operation_history(label=comment)

        for operation in history.operations:
            comment_payment = str(operation.label)

            if comment_payment == comment:
                return True

        return False

    def get_balance(self):
        user = self.client.account_info()

        return user.balance