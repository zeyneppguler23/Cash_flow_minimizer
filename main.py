from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

class Bank:
    def __init__(self, name):
        self.name = name
        self.net_amount = 0
        self.types = set()

class CashFlowMinimizer(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.add_widget(Label(text="Welcome to CASH FLOW MINIMIZER SYSTEM"))

        self.num_banks_input = TextInput(hint_text="Enter the number of banks", multiline=False)
        self.add_widget(self.num_banks_input)

        self.submit_banks_button = Button(text="Submit Banks")
        self.submit_banks_button.bind(on_press=self.submit_banks)
        self.add_widget(self.submit_banks_button)

        self.result_label = Label(text="")
        self.add_widget(self.result_label)

        self.banks_details = []
        self.bank_count = 0
        self.num_banks = 0
        self.input_banks = []
        self.index_of = {}
        self.max_num_types = 0
        self.graph = []

    def submit_banks(self, instance):
        self.num_banks = int(self.num_banks_input.text)
        self.result_label.text = f"Enter details for {self.num_banks} banks:"
        self.clear_widgets()

        for i in range(self.num_banks):
            layout = BoxLayout(orientation='horizontal')
            layout.add_widget(Label(text=f"Bank {i}: "))

            name_input = TextInput(hint_text="Name", multiline=False)
            layout.add_widget(name_input)

            modes_input = TextInput(hint_text="Payment Modes (comma separated)", multiline=False)
            layout.add_widget(modes_input)

            self.banks_details.append((name_input, modes_input))
            self.add_widget(layout)

        self.submit_details_button = Button(text="Submit Details")
        self.submit_details_button.bind(on_press=self.collect_bank_details)
        self.add_widget(self.submit_details_button)

    def collect_bank_details(self, instance):
        for i, (name_input, modes_input) in enumerate(self.banks_details):
            name = name_input.text
            modes = modes_input.text.split(',')

            input_bank = Bank(name)
            input_bank.types = set(modes)
            self.input_banks.append(input_bank)
            self.index_of[name] = i

            if i == 0:
                self.max_num_types = len(modes)

        self.clear_widgets()
        self.graph_input()

    def graph_input(self):
        self.result_label.text = "Enter transactions:"
        self.add_widget(self.result_label)

        self.num_transactions_input = TextInput(hint_text="Number of Transactions", multiline=False)
        self.add_widget(self.num_transactions_input)

        self.submit_transactions_button = Button(text="Submit Transactions")
        self.submit_transactions_button.bind(on_press=self.collect_transactions)
        self.add_widget(self.submit_transactions_button)

    def collect_transactions(self, instance):
        num_transactions = int(self.num_transactions_input.text)
        self.graph = [[0] * self.num_banks for _ in range(self.num_banks)]

        self.clear_widgets()

        self.transactions_input = []

        for i in range(num_transactions):
            layout = BoxLayout(orientation='horizontal')

            debtor_input = TextInput(hint_text="Debtor Bank", multiline=False)
            layout.add_widget(debtor_input)

            creditor_input = TextInput(hint_text="Creditor Bank", multiline=False)
            layout.add_widget(creditor_input)

            amount_input = TextInput(hint_text="Amount", multiline=False)
            layout.add_widget(amount_input)

            self.transactions_input.append((debtor_input, creditor_input, amount_input))
            self.add_widget(layout)

        self.calculate_button = Button(text="Calculate Minimum Cash Flow")
        self.calculate_button.bind(on_press=self.calculate_min_cash_flow)
        self.add_widget(self.calculate_button)

    def calculate_min_cash_flow(self, instance):
        for debtor_input, creditor_input, amount_input in self.transactions_input:
            debtor = debtor_input.text
            creditor = creditor_input.text
            amount = int(amount_input.text)
            self.graph[self.index_of[debtor]][self.index_of[creditor]] = amount

        # Call the cash flow minimizer function here
        minimize_cash_flow(self.num_banks, self.input_banks, self.index_of, len(self.transactions_input), self.graph, self.max_num_types)

class CashFlowApp(App):
    def build(self):
        return CashFlowMinimizer()

if __name__ == "__main__":
    CashFlowApp().run()
