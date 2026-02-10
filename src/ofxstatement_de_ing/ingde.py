import csv
import sys
import re
import datetime
import decimal

from ofxstatement import statement
from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.parser import StatementParser
from ofxstatement.statement import StatementLine


umlaute_dict = {
    '\xc3\xa4': 'ae',  # U+00E4      \xc3\xa4
    '\xc3\xb6': 'oe',  # U+00F6      \xc3\xb6
    '\xc3\xbc': 'ue',  # U+00FC      \xc3\xbc
    '\xc3\x84': 'Ae',  # U+00C4      \xc3\x84
    '\xc3\x96': 'Oe',  # U+00D6      \xc3\x96
    '\xc3\x9c': 'Ue',  # U+00DC      \xc3\x9c
    '\xc3\x9f': 'ss',  # U+00DF      \xc3\x9f
}


class IngDePlugin(Plugin):
    """ING DiBa Germany / Deutschland Plugin
    """

    def get_parser(self, filename):
        f = open(filename, 'r', encoding=self.settings.get("charset", "iso-8859-1"))
        parser = IngDeParser(f)
        return parser


class IngDeParser(CsvStatementParser):

    date_format = "%d.%m.%Y"
    mappings = dict()
    reader = None
    currency = None

    def format_iban(self, iban):
        return re.sub(r'\s+', '', iban, flags=re.UNICODE)

    def format_number_de(self, value: str):
        thousands_sep = '.'
        decimal_sep = ','
        return value.replace(thousands_sep, '').replace(decimal_sep, '.')

    def parse(self):
        """Main entry point for parsers

        super() implementation will call to split_records and parse_record to
        process the file.
        """
        with_saldo = False

        with self.fin:
            # initialize csv reader
            self.reader = csv.reader(self.fin, delimiter=';')

            # iterate over objects until we get to first important row
            for row in self.reader:

                # skip empty line
                if len(row) == 0:
                    continue

                # IBAN number
                if row[0] == 'IBAN':
                    account_id = self.format_iban(row[1])

                # Account name / type
                if row[0] == 'Kontoname':
                    account_type_ger = row[1]

                # bank id
                if row[0] == 'Bank':
                    bank_id = row[1]

                # date range
                if row[0] == 'Zeitraum':
                    start_date = datetime.datetime.strptime(row[1].split(' - ')[0], self.date_format)
                    end_date = datetime.datetime.strptime(row[1].split(' - ')[1], self.date_format)

                # starting saldo
                if row[0] == 'Saldo':
                    start_balance = decimal.Decimal(self.format_number_de(row[1]))
                    self.currency = row[2]
                    with_saldo = True

                # header of actual statement data
                # generate mapping
                if row[0] == 'Buchung':

                    for i, column in enumerate(row):

                        # date user initiated transaction
                        if column == 'Buchung':
                            self.mappings['date_user'] = i

                        # date transaction was posted to account
                        if column == 'Valuta':
                            self.mappings['date'] = i

                        # payee
                        if column == 'Auftraggeber/Empfänger':
                            self.mappings['payee'] = i

                        # transaction type (in german)
                        if column == 'Buchungstext':
                            self.mappings['trntype'] = i

                        # transaction description
                        if column == 'Verwendungszweck':
                            self.mappings['memo'] = i

                        # saldo
                        if column == 'Saldo':
                            self.mappings['saldo'] = i

                        # currency (this may appear twice if saldo is included,
                        # but that should be no problem, because we are interested
                        # in the second "Währung" column for the actual amount)
                        if column == 'Währung':
                            self.mappings['curr'] = i

                        # the actual amount
                        if column == 'Betrag':
                            self.mappings['amount'] = i

                    # break the loop over rows
                    break

            # check if saldo is present
            if not with_saldo:
                raise RuntimeError('CSV must be exported with saldo!')

            # parse each line
            stmt = super(IngDeParser, self).parse()

            # fill in bank infos
            stmt.account_id = account_id
            stmt.bank_id = bank_id
            stmt.currency = self.currency
            stmt.start_date = start_date
            stmt.end_date = end_date
            stmt.start_balance = start_balance

            # try to get account type
            if account_type_ger == 'Girokonto':
                stmt.account_type = "CHECKING"
            elif account_type_ger == 'Extra-Konto':
                stmt.account_type = "SAVINGS"

            # finalize statement
            statement.recalculate_balance(stmt)

            return stmt

    def split_records(self):
        """Return iterable object consisting of a line per transaction
        """
        return self.reader

    def parse_record(self, line):
        """Parse given transaction line and return StatementLine object
        """

        # fix german number format
        line[self.mappings['amount']] = self.format_number_de(line[self.mappings['amount']])

        # save german transaction type
        trntype_ger = line[self.mappings['trntype']]

        # default transaction type
        trntype = 'OTHER'

        # merchant initiated debit
        if trntype_ger == 'Lastschrift':
            trntype = 'DIRECTDEBIT'

        # income
        if trntype_ger == 'Gehalt/Rente':
            trntype = 'CREDIT'

        # credit
        if trntype_ger == 'Gutschrift':
            trntype = 'CREDIT'

        # repeated payment
        if trntype_ger == 'Dauerauftrag / Terminueberweisung':
            trntype = 'REPEATPMT'

        # money transfer
        if trntype_ger == 'Überweisung':
            trntype = 'XFER'

        # generic debit
        if trntype_ger == 'Abbuchung':
            trntype = 'DIRECTDEP'

        # overwrite transaction type
        line[self.mappings['trntype']] = trntype

        # throw error on different currency
        if line[self.mappings['curr']] != self.currency:
            raise ValueError('Different currencies are not supported!')

        # parse line elements using the mappings defined above (call parse_record() from parent class)
        stmtline = super(IngDeParser, self).parse_record(line)

        # generate id for statement
        id_date = stmtline.date.strftime('%Y%m%d')

        # create a hash from payee, memo, amount, saldo
        saldo = line[self.mappings['saldo']]
        id_hash = str(hash(stmtline.payee + stmtline.memo + str(stmtline.amount) + str(saldo)) % ((sys.maxsize + 1) * 2))

        # final id is constructed from date and hash (so hopefully this is unique)
        stmtline.id = id_date + id_hash

        return stmtline
