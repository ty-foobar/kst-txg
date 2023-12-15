from datetime import date, timedelta
from . import util

class Prof:
    def __init__(self, info: dict):
        self.info = info
        self.set_fund_code()
        self.concat_fund_name_fund_code()
        self.check_occupation()

    def set_fund_code(self):
        self.info['資金コード'] = self.info.get('資金コード', '')

    def concat_fund_name_fund_code(self):
        if not self.info['資金コード']:
            self.info['資金名・資金コード'] = self.info['資金名']
        else:
            self.info['資金名・資金コード'] = f'{self.info["資金名"]}・{self.info["資金コード"]}'

    def check_occupation(self):
        occupations = (
            '教授', '准教授', '専任講師', '助教', '特任教授', '特任准教授', '特任講師', '特任助教', 
            '客員教員', '研究員', '特別研究員（PD・RPD・SPD・CPD）', '特別研究員（DC２）', '特別研究員（DC１）', 
            '博士課程4年', '博士課程3年', '博士課程2年', '博士課程1年', 
            '修士課程2年', '修士課程1年', '学部6年', '学部5年', '学部4年', 'その他'
            )
        if self.info['職名'] not in occupations:
            string = '「職名」は次のいずれかにしてください: '
            for occupation in occupations:
                string += f'{occupation}, '
            util.exit_(string.rstrip(', '))

    def replacement(self, string: str):
        return str(self.info[string]) # str(arg): arg might be int

    def print_all(self):
        for key, val in self.info.items():
            print(f'{key}: {val}')

class Student:
    def __init__(self, info: dict):
        self.info = info
        self.check_major()
        self.check_course()
        self.check_year()
        self.check_bank_info()

    def check_major(self):
        majors = (
            '基礎理工学専攻', '総合デザイン工学専攻', '開放環境科学専攻', '機械工学科', '電気情報工学科', 
            '応用化学科', '物理情報工学科', '管理工学科', '数理科学科', '物理学科', '化学科', 
            'システムデザイン工学科', '情報工学科', '生命情報学科', '理工学研究科（リーディング）'
        )
        if self.info['専攻／学科'] not in majors:
            string = '「専攻／学科」は次のいずれかにしてください: '
            for major in majors:
                string += f'{major}, '
            util.exit_(string.rstrip(', '))

    def check_course(self):
        courses = ('博士', '修士', '学部')
        if self.info['課程'] not in courses:
            string = '「課程」は次のいずれかにしてください: '
            for course in courses:
                string += f'{course}, '
            util.exit_(string.rstrip(', '))

    def check_year(self):
        years = (1, 2, 3, 4)
        if self.info['学年'] not in years:
            string = '「学年」は次のいずれかにしてください: '
            for year in years:
                string += f'{year}, '
            util.exit_(string.rstrip(', '))

    def check_bank_info(self):
        if isinstance(self.info['口座番号'], int):
            self.info['口座番号'] = str(self.info['口座番号'])
        if '銀行' in self.info['銀行名']:
            util.exit_(f'銀行名「{self.info["銀行名"]}」から「銀行」を削除してください')
        if '支店' in self.info['支店名']:
            util.exit_(f'支店名「{self.info["支店名"]}」から「支店」を削除してください')
        if len(self.info['口座番号']) != 7:
            util.exit_('口座番号は7桁で指定してください')

    def set_account_numbers(self):
        for i, num in enumerate(self.info['口座番号'], start=1):
            self.info[f'口座番号{i}'] = num

    def replacement(self, string: str):
        return str(self.info[string]) # str(arg): arg might be int

    def print_all(self):
        for key, val in self.info.items():
            print(f'{key}: {val}')

class Day():
    def __init__(self, dateStr: str, route: str):
        date_ = self.format_date(dateStr)
        self.info = {
            '月': date_.month,
            '日': date_.day,
            '経路': route,
        }

    def format_date(self, dateStr: str):
        dateStrLst = dateStr.split('/')
        dateIntLst = (int(s) for s in dateStrLst)
        return date(*dateIntLst)

    def print_all(self):
        print(f'旅程 || {self.info["月"]}/{self.info["日"]} | {self.info["経路"]}')

class Tatekae():
    def __init__(self, what: str, num: int, amount: int, notes: str):
        self.info = {
            '内容': what,
            '個数': int(num),
            '金額': int(amount),
            '備考': notes,
        }

    def print_all(self):
        print(
            '立替 || '
           f'内容: {self.info["内容"]} | '
           f'個数: {self.info["個数"]} | '
           f'金額: {self.info["金額"]} | '
           f'備考: {self.info["備考"]}'
        )

class Trip():
    def __init__(self, info: dict, days: list[Day], tatekaes: list[Tatekae]):
        self.info = info
        self.days = days
        self.tatekaes = tatekaes
        self.check_bools()

    def check_bools(self):
        for key in ('保証人に連絡済', '国内用務', '海外保険に加入済'):
            if not isinstance(self.info[key], bool):
                util.exit_(f'「{key}」の値は True か False のブーリアン型にしてください')

    def set_num_days(self):
        firstDate = self.format_date(self.info['用務開始日'])
        lastDate = self.format_date(self.info['用務終了日'])
        self.info['出張日数'] = (lastDate - firstDate + timedelta(days = 1)).days

    def set_year_month_day(self, whatDay: str):
        if whatDay[-1] != '日':
            util.exit_(f'{whatDay} must end with "日"') # for internal
        what = whatDay[:-1] # e.g. '書類提出日'->'書類提出'
        date_ = self.format_date(self.info[whatDay])
        self.info[f'{what}年'] = date_.year
        self.info[f'{what}月'] = date_.month
        self.info[f'{what}日'] = date_.day

    def set_insurance(self):
        if self.info['国内用務']:
            self.info['海外保険に加入済'] = None

    def set_tatekae_total(self):
        total = 0
        for tatekae in self.tatekaes:
            total += tatekae.info['個数'] * tatekae.info['金額']
        self.info['立替金額合計'] = total

    def format_date(self, dateStr: str):
        dateStrLst = dateStr.split('/')
        dateIntLst = (int(s) for s in dateStrLst)
        return date(*dateIntLst)

    def replacement(self, string: str):
        if 'Bool' in string:
            return self.Bool_replacement(string[4:]) # 4 == len('Bool')
        elif 'Day' in string:
            return self.Day_replacement(string[3:]) # 3 == len('Day')
        elif 'Tatekae' in string:
            return self.Tatekae_replacement(string[7:]) # 7 == len('Tatekae')
        else:
            return str(self.info[string]) # str(arg): arg might be int

    def Bool_replacement(self, string: str):
        TorF, valName = string.split('-')
        if TorF == 'T' and self.info[valName] == True:
            return '●'
        elif TorF == 'F' and self.info[valName] == False:
            return '●'
        else: # includes self.info[valName] == None
            return ''

    def Day_replacement(self, string: str):
        rowNum, colName = string.split('-')
        if int(rowNum) > len(self.days):
            return ''
        else:
            indx = int(rowNum) - 1
            return str(self.days[indx].info[colName]) # str(arg): arg might be int

    def Tatekae_replacement(self, string: str):
        rowNum, colName = string.split('-')
        if int(rowNum) > len(self.tatekaes):
            return ''
        else:
            indx = int(rowNum) - 1
            return str(self.tatekaes[indx].info[colName]) # str(arg): arg might be int

    def print_all(self):
        for key, val in self.info.items():
            print(f'{key}: {val}')
        print('-' * 30)
        for item in self.days:
            item.print_all()
        print('-' * 30)
        for item in self.tatekaes:
            item.print_all()
