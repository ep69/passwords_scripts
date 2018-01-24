from scripts.analysisBase import AnalysisTemplate

import scripts.filter as data_filter
import scripts.table as data_table
import math


class PassfaultScoring(AnalysisTemplate):

    def runAnalysis(self):
        # Match passwords & lower score then 10000000
        self.setData(self.analyzer.data_set['all_passwords'])
        self.clearFilter()

        self.addFilter(data_filter.PCLOutputRegex({
            'Passfault': 'Match'
        }))
        self.addFilter(data_filter.ScoreHigher({
            'Passfault': 10000001
        }))
        self.applyFilter()

        table_1 = data_table.ComplexPassword(self.getData()).getTable(
            sortby='Passfault score',
            fields=[
                'Password',
                'Pwscore', 'Pwscore score',
                'Zxcvbn', 'Zxcvbn score',
                'Passfault', 'Passfault score',
            ],
            start=500,
            end=600
        )
        table_2 = data_table.SummaryScore(self.getData()).getTable(
            fields=[
                'Passfault score', 'Pwscore score', 'Zxcvbn score'
            ],
            start=0,
            end=150
        )
        self.printToFile(
            table_1,
            filename='outputs/' + self.__class__.__name__
        )
        self.printToFile(
            'Number of passwords: ' + str(len(self.getData())),
            filename='outputs/' + self.__class__.__name__
        )

        self.printToFile(
            table_2,
            filename='outputs/' + self.__class__.__name__
        )


class ZxcvbnPalindrom(AnalysisTemplate):

    def runAnalysis(self):
        self.setData(self.analyzer.data_set['all_passwords'])

        self.addFilter(data_filter.PCLOutputRegex({
            'Pwscore': 'The password is a palindrome'
        }))
        self.addFilter(data_filter.ChangePCLOutputByScore())
        self.applyFilter()

        table_1 = data_table.OverallSummary(self.getData()).getTable(
            start=0,
            end=40
        )

        self.printToFile(
            table_1,
            filename=None
        )

        self.clearFilter()
        self.addFilter(data_filter.ScoreHigher({
            'Zxcvbn': 3
        }))
        self.applyFilter()

        table_2 = data_table.ComplexPassword(self.getData()).getTable(
            sortby='Zxcvbn score',
            reversesort=True,
            fields=[
                'Password', 'Diff. char.', 'Char. classes', 'Length',
                'Pwscore', 'Pwscore score',
                'Zxcvbn', 'Zxcvbn score'
            ]
        )

        self.printToFile(
            table_2,
            filename=None
        )


class ZxcvbnDictionary(AnalysisTemplate):

    def runAnalysis(self):
        # Any dictionary word, especially Match in Zxcvbn
        self.setData(self.analyzer.data_set['all_passwords'])

        self.addFilter(data_filter.ChangePCLOutputByScore({
            'Zxcvbn': 3,
            'Pwscore': 40
        }))
        self.addFilter(data_filter.PCLOutputRegex({
            'CrackLib': 'dictionary word',
            'PassWDQC': 'dictionary',
            'Passfault': 'Match',
            'Pwscore': 'dictionary word'
        }))
        self.addFilter(data_filter.OriginalPCLOutputIsOk(['Zxcvbn']))
        self.applyFilter()

        table_1 = data_table.ComplexPassword(self.getData()).getTable(
            fields=[
                'Password',
                'CrackLib', 'PassWDQC', 'Pwscore', 'Passfault', 'Zxcvbn'
            ],
            start=0,
            end=100
        )
        table_2 = data_table.OverallSummary(self.getData()).getTable(
            start=0,
            end=10
        )
        self.printToFile(
            table_1,
            filename='outputs/' + self.__class__.__name__
        )
        self.printToFile(
            table_2,
            filename='outputs/' + self.__class__.__name__
        )

        # Dictionary word only in CrackLib, PassWDQC & Pwscore
        self.setData(self.analyzer.data_set['all_passwords'])
        self.clearFilter()

        self.addFilter(data_filter.ChangePCLOutputByScore({
            'Zxcvbn': 3,
            'Pwscore': 40
        }))
        self.addFilter(data_filter.PCLOutputRegex({
            'CrackLib': 'dictionary word',
            'PassWDQC': 'dictionary',
            'Pwscore': 'dictionary word'
        }))
        self.addFilter(data_filter.OriginalPCLOutputIsOk(['Zxcvbn']))
        self.applyFilter()

        table_1 = data_table.ComplexPassword(self.getData()).getTable(
            sortby='Zxcvbn score',
            fields=[
                'Password',
                'CrackLib', 'PassWDQC', 'Pwscore', 'Zxcvbn', 'Zxcvbn score'
            ],
            start=0,
            end=100
        )
        table_2 = data_table.OverallSummary(self.getData()).getTable(
            start=0,
            end=10
        )
        self.printToFile(
            table_1,
            filename='outputs/' + self.__class__.__name__
        )
        self.printToFile(
            table_2,
            filename='outputs/' + self.__class__.__name__
        )

        # PassWDQC - 'Dic. word', CrackLib - 'OK', Pwscore - 'OK'
        self.setData(self.analyzer.data_set['all_passwords'])
        self.clearFilter()

        self.addFilter(data_filter.ChangePCLOutputByScore())
        self.addFilter(data_filter.PCLOutputRegex({
            'PassWDQC': 'dictionary'
        }))
        #self.addFilter(data_filter.OriginalPCLOutputIsOk(['CrackLib']))
        #self.addFilter(data_filter.OriginalPCLOutputIsOk(['Pwscore']))
        self.applyFilter()

        table_1 = data_table.OverallSummary(self.getData()).getTable(
            fields=[
                'CrackLib accepted', 'CrackLib rejected',
                'CrackLib reasons of rejection',
                'PassWDQC accepted', 'PassWDQC rejected',
                'PassWDQC reasons of rejection',
                'Pwscore accepted', 'Pwscore rejected',
                'Pwscore reasons of rejection'
                ],
            start=0,
            end=7
        )
        self.printToFile(
            table_1,
            filename='outputs/' + self.__class__.__name__
        )

        # Dictionary word for every PCL
        self.setData(self.analyzer.data_set['all_passwords'])
        self.clearFilter()

        self.addFilter(data_filter.ChangePCLOutputByScore({
            'Zxcvbn': 3,
            'Pwscore': 40
        }))
        self.addFilter(data_filter.PCLOutputRegex({
            'CrackLib': 'dictionary word'
        }))
        self.addFilter(data_filter.PCLOutputRegex({
            'PassWDQC': 'dictionary'
        }))
        self.addFilter(data_filter.PCLOutputRegex({
            'Passfault': 'Match'
        }))
        self.addFilter(data_filter.PCLOutputRegex({
            'Pwscore': 'dictionary word'
        }))
        self.applyFilter()

        table_1 = data_table.ComplexPassword(self.getData()).getTable(
            fields=[
                'Password',
                'CrackLib', 'PassWDQC', 'Pwscore', 'Passfault',
                'Zxcvbn', 'Zxcvbn score'
            ],
            start=0,
            end=100
        )

        table_2 = data_table.OverallSummary(self.getData()).getTable(
            start=0,
            end=10
        )

        # Zxcvbn - OK passwords
        self.clearFilter()
        self.addFilter(data_filter.OriginalPCLOutputIsOk(['Zxcvbn']))
        self.applyFilter()
        table_3 = data_table.ComplexPassword(self.getData()).getTable(
            fields=[
                'Password',
                'CrackLib', 'PassWDQC', 'Pwscore', 'Zxcvbn', 'Passfault'
            ],
            start=0,
            end=100
        )

        self.printToFile(
            table_1,
            filename='outputs/' + self.__class__.__name__
        )
        self.printToFile(
            table_2,
            filename='outputs/' + self.__class__.__name__
        )
        self.printToFile(
            table_3,
            filename='outputs/' + self.__class__.__name__
        )


class PassfaultKeyboardSequence(AnalysisTemplate):

    def runAnalysis(self):
        # Passfault define passwords with keyboard sequences
        # other libaries accept these passwords
        # Remove Match from passfault
        self.setData(self.analyzer.data_set['all_passwords'])

        self.addFilter(data_filter.ChangePCLOutputByScore({
            'Pwscore': 40,
            'Zxcvbn': 3
        }))
        self.addFilter(data_filter.OriginalPCLOutputIsOk(['CrackLib']))
        self.addFilter(data_filter.OriginalPCLOutputIsOk(['PassWDQC']))
        self.addFilter(data_filter.OriginalPCLOutputIsOk(['Pwscore']))
        self.addFilter(data_filter.OriginalPCLOutputIsOk(['Zxcvbn']))

        self.addFilter(data_filter.PCLOutputDoesNotContainString({
            'Passfault': 'Match'
        }))
        self.addFilter(data_filter.PCLOutputRegex({
            'Passfault': 'Keyboard'
        }))
        self.applyFilter()

        table_1 = data_table.ComplexPassword(self.getData()).getTable(
            sortby='Passfault score',
            fields=[
                'Password', 'CrackLib', 'PassWDQC',
                'Passfault', 'Passfault score',
                'Pwscore', 'Pwscore score',
                'Zxcvbn', 'Zxcvbn score'
                ]
        )

        self.printToFile(
            table_1,
            filename='outputs/' + self.__class__.__name__
        )

        # Second table, lower score by Passfault pcl, and OK by others pcls
        self.setData(self.analyzer.data_set['all_passwords'])
        self.clearFilter()

        self.addFilter(data_filter.ChangePCLOutputByScore({
            'Pwscore': 40,
            'Zxcvbn': 3
        }))
        self.addFilter(data_filter.ScoreLower({
            'Passfault': 2500000
        }))
        self.addFilter(data_filter.OriginalPCLOutputIsOk(['Pwscore']))
        self.addFilter(data_filter.OriginalPCLOutputIsOk(['Zxcvbn']))
        self.addFilter(data_filter.PCLOutputDoesNotContainString({
            'Passfault': 'Match'
        }))
        self.applyFilter()

        table_2 = data_table.ComplexPassword(self.getData()).getTable(
            sortby='Pwscore score',
            fields=[
                'Password', 'CrackLib', 'PassWDQC',
                'Passfault', 'Passfault score',
                'Pwscore', 'Pwscore score',
                'Zxcvbn', 'Zxcvbn score'
                ]
        )
        table_3 = data_table.OverallSummary(self.getData()).getTable()
        
        self.printToFile(
            table_2,
            filename='outputs/' + self.__class__.__name__
        )
        self.printToFile(
            table_3,
            filename='outputs/' + self.__class__.__name__
        )


class PassfaultOneMatch(AnalysisTemplate):

    def runAnalysis(self):
        self.setData(self.analyzer.data_set['all_passwords'])

        self.addFilter(data_filter.PCLOutputDoesNotContainString({
            'Passfault': ','
        }))
        self.addFilter(data_filter.PCLOutputRegex({
            'Passfault': 'Match'
        }))
        self.addFilter(data_filter.ScoreHigher({
            'Zxcvbn': 3
        }))
        self.applyFilter()

        table = data_table.ComplexPassword(self.getData()).getTable(
            sortby='Zxcvbn score',
            reversesort=True
        )
        self.printToFile(
            table,
            filename='outputs/' + self.__class__.__name__
        )


class PassfaultMatchWorstPasswords(AnalysisTemplate):

    def runAnalysis(self):
        self.setData(self.analyzer.data_set['all_passwords'])

        self.addFilter(data_filter.PCLOutputDoesNotContainString({
            'Passfault': ','
        }))
        self.addFilter(data_filter.PCLOutputRegex({
            'Passfault': 'worst-passwords'
        }))
        self.addFilter(data_filter.ChangePCLOutputByScore({
            'Pwscore': 40,
            'Zxcvbn': 3
        }))
        self.addFilter(data_filter.OriginalPCLOutputIsOk([
            'CrackLib', 'PassWDQC', 'Pwscore', 'Zxcvbn'
        ]))
        self.applyFilter()

        table = data_table.ComplexPassword(self.getData()).getTable()
        self.printToFile(
            table,
            filename='outputs/' + self.__class__.__name__
            )


class ZxcvbnCommonPasswords(AnalysisTemplate):

    def runAnalysis(self):
        # Passwords that only Zxcvbn recognize as 'commonly used password'
        # and are accepteb by other libraries
        self.setData(self.analyzer.data_set['all_passwords'])

        self.addFilter(data_filter.PCLOutputRegex({
            'Zxcvbn': 'commonly used password'
        }))

        self.addFilter(data_filter.PCLOutputDoesNotContainString({
            'CrackLib': 'dictionary word'
        }))
        self.addFilter(data_filter.PCLOutputDoesNotContainString({
            'Pwscore': 'dictionary word'
        }))
        self.addFilter(data_filter.PCLOutputDoesNotContainString({
            'PassWDQC': 'dictionary'
        }))
        self.addFilter(data_filter.PCLOutputDoesNotContainString({
            'Passfault': 'Match'
        }))

        self.addFilter(data_filter.ChangePCLOutputByScore({
            'Pwscore': 40
        }))
        self.addFilter(data_filter.OriginalPCLOutputIsOk([
            'CrackLib', 'PassWDQC', 'Pwscore'
        ]))
        self.applyFilter()

        table_1 = data_table.OverallSummary(self.getData()).getTable(
            start=0,
            end=20
        )
        table_2 = data_table.ComplexPassword(self.getData()).getTable()
        self.printToFile(
            table_1,
            filename='outputs/' + self.__class__.__name__
            )
        self.printToFile(
            table_2,
            filename='outputs/' + self.__class__.__name__
            )

        # Passwords are accepted by PassWDQC or Pwscore
        self.clearFilter()
        self.addFilter(data_filter.OriginalPCLOutputIsOk([
            'PassWDQC', 'Pwscore'
        ]))
        self.applyFilter()

        table_3 = data_table.ComplexPassword(self.getData()).getTable(
            fields=[
                'Password', 'Diff. char.', 'Char. classes', 'Length',
                'CrackLib', 'PassWDQC',
                'Passfault', 'Passfault score',
                'Pwscore', 'Pwscore score',
                'Zxcvbn', 'Zxcvbn score'
            ]
        )
        self.printToFile(
            table_3,
            filename='outputs/' + self.__class__.__name__
            )

        # Passwords are accepted by both PCLs PassWDQC and Pwscore
        self.clearFilter()
        self.addFilter(data_filter.OriginalPCLOutputIsOk([
            'PassWDQC'
        ]))
        self.addFilter(data_filter.OriginalPCLOutputIsOk([
            'Pwscore'
        ]))
        self.applyFilter()

        table_4 = data_table.ComplexPassword(self.getData()).getTable(
            fields=[
                'Password', 'Diff. char.', 'Char. classes', 'Length',
                'CrackLib', 'PassWDQC',
                'Passfault', 'Passfault score',
                'Pwscore', 'Pwscore score',
                'Zxcvbn', 'Zxcvbn score'
            ]
        )
        self.printToFile(
            table_4,
            filename='outputs/' + self.__class__.__name__
            )


class EmailAddresses(AnalysisTemplate):

    def runAnalysis(self):
        self.setData(self.analyzer.data_set['all_passwords'])

        self.addFilter(data_filter.PasswordRegex('^.+\@.+\..+$'))
        self.addFilter(data_filter.ChangePCLOutputByScore())
        self.applyFilter()

        table_1 = data_table.OverallSummary(self.getData()).getTable()
        table_2 = data_table.ComplexPassword(self.getData()).getTable()
        self.printToFile(
            table_1,
            filename='outputs/' + self.__class__.__name__
        )
        self.printToFile(
            table_2,
            filename='outputs/' + self.__class__.__name__
        )


class CracklibPwscorePattern(AnalysisTemplate):

    def runAnalysis(self):
        # Password pattern 2NXL2N, X>7, Length > 10
        self.setData(self.analyzer.data_set['all_passwords'])

        self.addFilter(data_filter.PasswordRegex('^\d\d[a-zA-Z]{7,}\d\d$'))
        self.addFilter(data_filter.PasswordLengthHigher(10))
        self.addFilter(data_filter.ChangePCLOutputByScore({
            'Pwscore': 40,
            'Zxcvbn': 3
        }))
        self.applyFilter()

        table_1 = data_table.OverallSummary(self.getData()).getTable()
        table_2 = data_table.ComplexPassword(self.getData()).getTable()
        self.printToFile(
            table_1,
            filename='outputs/' + self.__class__.__name__
        )
        self.printToFile(
            table_2,
            filename='outputs/' + self.__class__.__name__
        )


class PassWDQCPasswordLength(AnalysisTemplate):

    def runAnalysis(self):
        self.setData(self.analyzer.data_set['all_passwords'])

        self.addFilter(data_filter.ChangePCLOutputByScore({
            'Pwscore': 40,
            'Zxcvbn': 3
        }))
        self.applyFilter()

        for pass_length in range(10, 21):
            self.clearFilter()
            self.addFilter(data_filter.PasswordLengthHigher(pass_length))
            self.applyFilter()
            table_1 = data_table.OverallSummary(self.getData()).getTable(
                start=0,
                end=15
            )
            self.printToFile(
                "Password length == " + str(pass_length),
                filename='outputs/' + self.__class__.__name__
            )
            self.printToFile(
                table_1,
                filename='outputs/' + self.__class__.__name__
            )

            if (pass_length in [15, 20]):
                table_2 = data_table.ComplexPassword(self.getData()).getTable(
                    fields=[
                        'Password', 'Length',
                        'CrackLib', 'PassWDQC',
                        'Passfault', 'Passfault score',
                        'Pwscore', 'Pwscore score',
                        'Zxcvbn', 'Zxcvbn score'
                    ]
                )
                self.printToFile(
                    table_2,
                    filename='outputs/' + self.__class__.__name__
                )


class CracklibPwScoreLowPasswordScore(AnalysisTemplate):

    def runAnalysis(self):
        self.setData(self.analyzer.data_set['all_passwords'])

        self.addFilter(data_filter.ChangePCLOutputByScore())
        self.addFilter(data_filter.PCLOutputRegex({
            'Pwscore': 'Low password score'
        }))
        self.applyFilter()

        table_1 = data_table.OverallSummary(self.getData()).getTable(
            start=0,
            end= 25,
            fields=[
                'CrackLib accepted', 'CrackLib rejected',
                'CrackLib reasons of rejection',
                #'PassWDQC accepted', 'PassWDQC rejected',
                #'PassWDQC reasons of rejection',
                #'Passfault accepted', 'Passfault rejected',
                #'Passfault reasons of rejection',
                'Pwscore accepted', 'Pwscore rejected',
                'Pwscore reasons of rejection',
                'Zxcvbn accepted', 'Zxcvbn rejected',
                'Zxcvbn reasons of rejection'
            ]
        )
        self.printToFile(
            table_1,
            filename='outputs/' + self.__class__.__name__
        )


class TestAnalysis(AnalysisTemplate):

    def runAnalysis(self):
        pass
        '''
        self.setData(self.analyzer.data_set['all_passwords'])

        self.addFilter(data_filter.ConvertPassfaultScoreByLogBase())
        self.applyFilter()

        table = data_table.SummaryScore(self.getData()).getTable()
        self.printToFile(
            table,
            filename='outputs/' + self.__class__.__name__
        )
        '''
