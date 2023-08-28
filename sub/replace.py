import os, shutil
from . import util
from .cls import Prof, Student, Trip

def check_info_prompt(prof: Prof, student: Student, trip: Trip):
    print('次の情報が合っているか確認してください:\n')
    prof.print_all()
    print('=' * 30)
    student.print_all()
    print('=' * 30)
    trip.print_all()
    inputStr = input('\n上の情報は合っていますか？ [y/n]: ')
    print()
    if not inputStr.lower() == 'y':
        util.exit_('プログラムを終了します')

def set_student_trip(student: Student, trip: Trip):
    student.set_account_numbers()
    trip.set_num_days() # before trip.set_year_month_day()
    trip.set_year_month_day('書類提出日')
    trip.set_year_month_day('用務開始日')
    trip.set_year_month_day('用務終了日')
    trip.set_insurance()
    trip.set_tatekae_total()

def mk_tmp_dir():
    tmpDir = util.tmp_dir()
    shutil.copytree('template', tmpDir)

def zip_tmp_dir(trip: Trip):
    baseName = f'{trip.info["研究機関／学会活動の名称"]}_事前'
    xlFormat = util.xl_format()
    if os.path.isfile(f'{baseName}.{xlFormat}'):
        print(f'次のファイルは既に存在します: {baseName}.{xlFormat}')
        inputStr = input('上書きしますか？ [y/n]: ')
        print()
        if not inputStr.lower() == 'y':
            util.exit_('プログラムを終了します')
    tmpFormat = util.tmp_format()
    tmpDir = util.tmp_dir()
    shutil.make_archive(baseName, tmpFormat, tmpDir) # does not accept 'xlsx' format
    os.rename(f'{baseName}.{tmpFormat}', f'{baseName}.{xlFormat}')
    print(f'保存先: {baseName}.{xlFormat}\n')
    print(
        '*注意:\n'
        '「立替払い精算」の書類では、資金名が「5. その他」に記入されています。資金が'
        '「1. 教育研究費」「2. 指定寄付」「3. 受託研究」「4. 預り金」'
        'のいずれかの場合は、出力ファイルを直接編集してください。'
    )

def rm_tmp_dir():
    tmpDir = util.tmp_dir()
    shutil.rmtree(tmpDir)

def replace(prof: Prof, student: Student, trip: Trip, filePath: str):
    content = ''
    with open(filePath, 'r', encoding='utf-8') as file:
        for line in file:
            content += line
    chunks = content.split('##')
    for i, chunk in enumerate(chunks):
        if not chunk:
            continue
        sign = chunk[0]
        string = chunk[1:]
        if sign == '%':
            chunks[i] = prof.replacement(string)
        elif sign == '*':
            chunks[i] = student.replacement(string)
        elif sign == '$':
            chunks[i] = trip.replacement(string)
        else:
            continue
    with open(filePath, 'w', encoding='utf-8') as file:
        file.write(''.join(chunks))

def main(prof: Prof, student: Student, trip: Trip):
    check_info_prompt(prof, student, trip) # before set_student_trip()
    set_student_trip(student, trip)
    mk_tmp_dir()

    tmpDir = util.tmp_dir()
    replace(prof, student, trip, os.path.join(tmpDir, 'xl', 'sharedStrings.xml'))
    for i in range(1, 1000): # upper bound: any num. much larger than num. of sheets
        sheet = os.path.join(tmpDir, 'xl', 'worksheets', f'sheet{i}.xml')
        if not os.path.isfile(sheet):
            break
        replace(prof, student, trip, sheet)

    zip_tmp_dir(trip)
    rm_tmp_dir()
