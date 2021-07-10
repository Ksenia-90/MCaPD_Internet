from pprint import pprint

from ScrapperService import ScrapperService
from VacancyRepository import VacancyRepository


class VacancyService:

    @staticmethod
    def upload_vacancies(vacancy_on_page, pages_size, search_string, list_sites):
        scrapper_service = ScrapperService(vacancy_on_page, pages_size)
        res = scrapper_service.scrap_vacancies(search_string, list_sites)
        with VacancyRepository() as vacancy_repository:
            return vacancy_repository.insert_vacancies(res)

    @staticmethod
    def get_vacancies_on_qt_sum(salary, not_exist_salary):
        with VacancyRepository() as vacancy_repository:
            return vacancy_repository.get_qt_sum(salary, not_exist_salary)


if __name__ == '__main__':
    vacancy_service = VacancyService()
    pprint(vacancy_service.upload_vacancies(30, 1, "python", ["hh.ru", "superjob.ru"]).bulk_api_result)
    pprint(vacancy_service.get_vacancies_on_qt_sum(320000, False))
