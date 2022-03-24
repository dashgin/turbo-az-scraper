from urllib.parse import urlparse

import bs4
import requests

from utils.terminal_colors import BColors


def convert_to_standard_form(phone_number: str, country_code: str, allowed_operator_codes: list) -> str:
    """
    Convert phone number to standard form.

    :param phone_number:
    :param country_code:
    :param allowed_operator_codes:
    :return: str

    Example:
    >>> convert_to_standard_form('(051) 511-51-51', "+994")
    '+994515115151'
    """
    _allowed_operator_codes = allowed_operator_codes or [
        "50",
        "51",
        "55",
        "60",
        "70",
        "77",
        "99",
    ]
    phone_number = phone_number.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
    if phone_number.startswith('0') or phone_number.startswith('+'):
        phone_number = phone_number[1:]
    if phone_number[0:2] in _allowed_operator_codes:
        phone_number = country_code + phone_number
    else:
        return ''
    return phone_number


def get_numbers(
        base_url: str,
        page_query_param: str,
        not_found_class: str,
        item_link_class: str,
        store_item_link_class: str,
        item_class: str,
        first_page: int = 1,
        end_page: int = 1,

) -> dict:
    """
    Get the number of pages for a given url.


    :param base_url:
    :param first_page:
    :param end_page:
    :param item_link_class:
    :param item_class:
    :param store_item_link_class:
    :param page_query_param:
    :param not_found_class:
    :return: dict

    Example:
    >>> get_numbers(
    ...     base_url='https://turbo.az/autos',
    ...     page_query_param='page',
    ...     not_found_class='not_found',
    ...     item_link_class='products-i__link',
    ...     item_class='phone',
    ...     first_page=1,
    ...     end_page=1
    ... )
    {
        'url': 'https://turbo.az/autos',
        'result': [
            {
                'url': 'https://turbo.az/autos/6020480-porsche-cayenne-gts',
                'phone_numbers': [
                    '+994000000000',
                    '+994111111111',
                    '+994222222222',
                    '+994333333333'
                ]
            },
            ...
        ]
    }

    """

    _data_dict = {
        "url": base_url,
        "result": []
    }

    while first_page <= end_page:
        _url = f"{base_url}?{page_query_param}={first_page}"
        response = requests.get(_url)

        print(f'{BColors.OK_BLUE}[+]{BColors.END} Scccraping page {BColors.OK_GREEN}{first_page}{BColors.END}')

        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        # NOT FOUND
        if soup.find("div", {"class": not_found_class}) is not None:
            print(f'{BColors.FAIL}[-]{BColors.END} Page not found, exiting...')
            return _data_dict

        _page_links = soup.find_all('a', {'class': item_link_class})

        for _p_l in _page_links:
            _data = {
                "url": "",
                "phone_numbers": []
            }
            print(
                f'{BColors.OK_GREEN}[+]{BColors.END} Getting data for {BColors.OK_GREEN}{_p_l.get("href")}{BColors.END}'
            )

            _page_link = _p_l.get('href') if _p_l.get("href").startswith('/') else f"/{_p_l.get('href')}"

            _url = urlparse(base_url)

            page_link = f"{_url.scheme}://{_url.netloc}{_page_link}"
            _page_response = requests.get(page_link)

            _page_soup = bs4.BeautifulSoup(_page_response.text, 'html.parser')

            items = _page_soup.find_all('a', {'class': item_class}) or _page_soup.find_all('a', {
                'class': store_item_link_class})

            _data['url'] = page_link
            for i in items:
                _data['phone_numbers'].append(
                    convert_to_standard_form(i.text, "+994", ["50", "51", "55", "60", "70", "77", "99"]))

            _data_dict['result'].append(_data)

        first_page += 1

    print("[+] Done")
    return _data_dict

# class BaseScraper:
#     first_page: int = 1
#     end_page: int = 1
#     _not_found_class: str = None
#     _page_query_param: str = None
#
#     def get_page_query_param(self) -> str:
#         return self._page_query_param
#
#     def get_not_found_class(self) -> str:
#         return self._not_found_class
