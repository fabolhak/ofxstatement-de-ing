import csv
import itertools

from ofxstatement import statement
from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.parser import StatementParser
from ofxstatement.statement import StatementLine

class IngDePlugin(Plugin):
    """ING DiBa Germany / Deutschland Plugin
    """

    def get_parser(self, filename):
        f = open(filename, 'r', encoding=self.settings.get("charset", "ISO-8859-1"))
        parser = IngDeParser(f)
        return parser

class IngDeParser(CsvStatementParser):

    date_format = "%d.%m.%Y"
    mappings = {
        #'date_user':  0, # doesn't work for some reason
        'date':       1,
        'payee':      2,
        'memo':       4,
        'amount':     5
    }

    reader = None
    id = 0
    currency = None
    
    def parse(self):
        """Main entry point for parsers

        super() implementation will call to split_records and parse_record to
        process the file.
        """

        # initialize csv reader
        self.reader = csv.reader(self.fin, delimiter=';')

        # skip first three lines
        self.reader = itertools.islice(self.reader, 3, None)

        # get bank / account details
        account_id = self.reader.__next__()[1]     # account id = IBAN
        germantype = self.reader.__next__()[1]     # account type (german name)
        bank_id    = self.reader.__next__()[1]     # bank id

        # skip next lines
        self.reader = itertools.islice(self.reader, 7, None)

        # check wether saldo is included in csv file
        if "Saldo" != self.reader.__next__()[5]:
            raise ValueError('Please export CSV with Saldo!')

        # parse each line
        stmt = super(IngDeParser, self).parse()

        # fill in bank infos
        stmt.account_id = account_id.replace(" ", "")
        stmt.bank_id = bank_id
        stmt.currency = self.currency

        # try to get account type
        if "Girokonto" == germantype:
            stmt.account_type = "CHECKING"
        elif "Extra-Konto" == germantype:
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

        # check currency
        if None == self.currency:
            self.currency = line[8]
        elif self.currency != line[8] and self.currency != line[6]:
            raise ValueError('Different currencies are not supported!')

        # fix german number format
        line[5] = line[5].replace(".","").replace(",",".") 
        
        # parse line elements using the mappings defined above (call parse_record() from parent class)
        stmtline = super(IngDeParser, self).parse_record(line)

        # check if debit or credit
        stmtline.trntype = 'DEBIT' if stmtline.amount < 0 else 'CREDIT'

        # generate id for statement
        stmtline.id = str(self.id)
        self.id = self.id + 1

        return stmtline
