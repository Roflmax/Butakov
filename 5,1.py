import csv
import re
from datetime import datetime
from prettytable import PrettyTable, ALL
from rofl import rofl
#Текст для задания ура
class DataSet:


      def __init__(self, file_name: str):

              self.file_name = file_name
              self.vacancies_objects = []

              with open(file_name, encoding='utf-8-sig') as f:
                  rows_count = len(list(csv.reader(open(file_name, encoding='utf-8-sig'))))
                  if rows_count == 1:
                      print("Нет данных")
                      return
                  if rows_count == 0:
                      print("Пустой файл")
                      return
                  reader = csv.reader(f)
                  headers = next(reader)
                  fil_ed = filter(lambda row: len(row) == len(headers) and '' not in row, reader)
                  self.vacancies_objects = [Vacancy(dict(zip(headers, row))) for row in fil_ed]


class Vacancy:

      def __init__(self, row: dict):

             self.name = row['name']
             self.description = self.__clr_desc(row['description'])
             self.key_skills = row['key_skills'].split('\n')
             self.experience_id = fie_ru[row['experience_id']]
             self.premium = fie_ru.get(row['premium'], row['premium'])
             self.employer_name = row['employer_name']
             self.salary = Salary(row)
             self.area_name = row['area_name']
             self.published_at = datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z')

      def get_l(self) -> list:
             return [fie_ru.get(value, value) for value in [
                 self.name,
                 self.description,
                 '\n'.join(self.key_skills),
                 self.experience_id,
                 self.premium,
                 self.employer_name,
                 self.salary.get_string(),
                 self.area_name,
                 self.published_at.strftime('%d.%m.%Y')
             ]]

      @staticmethod
      def __clr_desc(description: str) -> str:
             description = re.sub('<.*?>', '', description)
             return ' '.join(description.split())


class Salary:
    __curr_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }

    def __init__(self, row: dict):
        self.salary_from =  int(float(row['salary_from']))
        self.salary_to =  int(float(row['salary_to']))
        self.salary_gross =  row['salary_gross']
        self.salary_currency =  row['salary_currency']

    def get_string(self):
        minn =  self.__slice(self.salary_from)
        maxx =  self.__slice(self.salary_to)
        vichet =  "Без вычета налогов" if self.salary_gross == 'True' else "С вычетом налогов"
        return f"{minn} - {maxx} ({fie_ru[self.salary_currency]}) ({vichet})"

    def get_rubl(self):
        a=self.salary_from + self.salary_to
        b=self.__curr_rub[self.salary_currency]
        return a / 2 * b

    @staticmethod
    def __slice(number: int) -> str:
        stri = str(number)[::-1]
        hod = 3
        return ' '.join([stri[i:i + hod] for i in range(0, len(stri), hod)])[::-1]


class uinput:
    __colum_filter = {
        "key_skills": lambda vacancy, value: set(value.split(', ')).
        issubset(vacancy.key_skills),
        "salary": lambda vacancy, value: vacancy.salary.
        salary_from <= int(value) <= vacancy.salary.salary_to,
        "salary_currency": lambda vacancy, value: vacancy.salary.
        salary_currency == russ_field[value],
        "published_at": lambda vacancy, value: vacancy.published_at.
        strftime('%d.%m.%Y') == value,
    }
    __colum_sort = {
        "key_skills": lambda vacancy: len(vacancy.key_skills),
        "experience_id": lambda vacancy: re.sub('\\D', '', vacancy.experience_id),
        "salary": lambda vacancy: vacancy.salary.get_rubl(),
        "published_at": lambda vacancy: vacancy.published_at,
    }

    def __init__(self):
        self.file_name = input("Введите название файла: ")
        self.filtr_inp = input("Введите параметр фильтрации: ")
        self.sort_input = input("Введите параметр сортировки: ")
        self.sort_revers_inp = input("Обратный порядок сортировки (Да / Нет): ")
        self.tabl_len_inp = input("Введите диапазон вывода: ")
        self.tabl_field_inp = input("Введите требуемые столбцы: ")

    def prin_tabl(self):
        headers = [fie_ru[header] for header in [
            'name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary', 'area_name',
            'published_at']]
        if not self.__corr_inp():
            return
        data = DataSet(self.file_name).vacancies_objects
        if not data:
            return
        data = self.__filt_dat(data)
        if not data:
            print("Ничего не найдено")
            return
        data = self.__sort_dat(data)
        table = PrettyTable(['№'] + headers, align='l', hrules=ALL, max_width=20)
        for i, row in enumerate(data):
            table.add_row([str(i + 1)] + list(map(self.__cut_len, row.get_l())))
        if self.tabl_len_inp:
            tabl_len = self.tabl_len_inp.split()
            if len(tabl_len) > 0:
                table.start = int(tabl_len[0]) - 1
            if len(tabl_len) > 1:
                table.end = int(tabl_len[1]) - 1
        if self.tabl_field_inp:
            table.fields = ['№'] + self.tabl_field_inp.split(', ')
        print(table.get_string().replace('\xa0', ' '))

    def __corr_inp(self) -> bool:
        if self.filtr_inp:
            if ': ' not in self.filtr_inp:
                print("Формат ввода некорректен")
                return False
            if self.filtr_inp.split(': ')[0] not in fie_ru.values():
                print("Параметр поиска некорректен")
                return False
        if self.sort_input:
            if self.sort_input not in fie_ru.values():
                print("Параметр сортировки некорректен")
                return False
            if self.sort_revers_inp not in ['', 'Да', 'Нет']:
                print("Порядок сортировки задан некорректно")
                return False
        return True

    def __filt_dat(self, data: list) -> list:
        if not self.filtr_inp:
            return data
        column_filter, value_filter = self.filtr_inp.split(': ')
        column_filter = russ_field[column_filter]
        filter_func = self.__colum_filter.get(column_filter, lambda x, y: getattr(x, column_filter) == y)
        return list(filter(lambda vacancy: filter_func(vacancy, value_filter), data))

    def __sort_dat(self, data: list) -> list:
        if not self.sort_input:
            return data
        column_sort = russ_field[self.sort_input]
        sort_func = self.__colum_sort.get(column_sort, lambda vacancy: getattr(vacancy, column_sort))
        is_reverse = True if self.sort_revers_inp == 'Да' else False
        return list(sorted(data, key=sort_func, reverse=is_reverse))

    @staticmethod
    def __cut_len(stri: str) -> str:
        max_length = 100
        if len(stri) > max_length:
            return f"{stri[:max_length]}..."
        return stri


fie_ru = {
    "True": "Да", "False": "Нет",

    "name": "Название", "description": "Описание", "key_skills": "Навыки", "experience_id": "Опыт работы",
    "premium": "Премиум-вакансия", "employer_name": "Компания", "salary_from": "Нижняя граница вилки оклада",
    "salary_to": "Верхняя граница вилки оклада", "salary_gross": "Оклад указан до вычета налогов",
    "salary_currency": "Идентификатор валюты оклада", "area_name": "Название региона",
    "published_at": "Дата публикации вакансии", "salary": "Оклад",

    "noExperience": "Нет опыта", "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет", "moreThan6": "Более 6 лет",

    "AZN": "Манаты", "BYR": "Белорусские рубли", "EUR": "Евро", "GEL": "Грузинский лари", "KGS": "Киргизский сом",
    "KZT": "Тенге", "RUR": "Рубли", "UAH": "Гривны", "USD": "Доллары", "UZS": "Узбекский сум",
}
russ_field = {v: k for k, v in fie_ru.items()}
if __name__ == "__main__":
    input_con = uinput()
    input_con.prin_tabl()