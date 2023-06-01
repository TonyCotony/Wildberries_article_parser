import asyncio

import aiohttp


async def async_parse(url: str, article: int) -> bool or dict:
    """
    Асинхронные запросы через aiohttp. После получения ответа, прогоняет текст через другие функции
    с целью найти искомый артикул

    принимает:
    ссылку,
    номер искомого артикула

    Возвращает ложь, если артикула не найден,
    если найден, то возвращает словарь с номером страницы и позицией товара на ней
    """
    async with aiohttp.request("GET", url) as response:
        if response.status == 200:

            check = check_article(
                text=await response.text(),
                article=article
            )

            if not check:
                return False

            else:
                page = get_page_number_from_link(link=url)
                info = {
                    # 'status': 1,
                    'page': page,
                    'position on the page': check
                }
                return info

        else:
            print(f'failed - {response.status}, {response.content}')


def get_page_number_from_link(link: str) -> int:
    """
    Извлекает номер страницы из ссылки на нее
    принимает ссылку в виде строки
    возвращает число
    """
    try:
        num = int(link.split('page=')[1].split('&')[0])
        print(link.split('page=')[1].split('&'))
        print(num)
        return num
    except IndexError:
        return 1


def check_article(text: str, article: int) -> False or int:
    """
    Проверяет наличие искомого артикула в выгрузке со страницы
    принимает текст из запроса, артикул искомого товара
    возвращает ложь, если не нашел совпадения с искомым артикулом
    """
    data = text.split(',')
    count = 0
    for _ in data:
        if _.startswith('"id":') and '}' not in _:
            count += 1
            # print(_)
            article_from_list = int(_.split(':')[1])
            if article == article_from_list:
                return count
    return False


async def get_info(products_group: str, article: int) -> bool or dict:
    """
    Функция формирует и отправляет список ссылок для запросов,
    в случае успешного нахождения артикула возвращает словарь со страницей и позицией товара на странице

    принимает:
    Название группы товаров для поиска
    Искомый артикул

    возвращает:
    ложь, если в 50 первых страницах(по 100 товаров) не найден нужный артикул
    словарь с номером страницы и позицией искомого артикула
    """
    link_first = f'https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=no_test&TestID=no_test&appType=1&curr=rub&dest=-1257786&page=2&query={products_group}&regions=80,38,4,64,83,33,68,70,69,30,86,75,40,1,66,110,22,31,48,71,114&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false'
    urls = [link_first]
    for _ in range(2, 51):
        urls += [link_first.replace('&query=', f'&page={_}&query=')]
    data = []

    for _ in range(len(urls)):
        data += [await async_parse(url=urls[_], article=article)]
    print(data)
    for _ in data:
        if type(_) == dict:
            return _

    return False
