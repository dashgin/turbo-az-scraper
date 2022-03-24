from django.http import JsonResponse
from django.views.decorators.http import require_safe, require_POST
from django.views.decorators.csrf import csrf_exempt

from utils.scraper.phone_number_scaper import get_numbers
from utils.terminal_colors import BColors
from .models import MacID, PhoneNumber


def check_phone_unique(phone_number):
    if PhoneNumber.objects.filter(phone_number__icontains=phone_number).exists():
        return False
    return True


@require_safe
def get_numbers_view(request):
    url = request.GET.get('url')
    first_page = request.GET.get('first_page')
    end_page = request.GET.get('end_page')

    if url is None or first_page is None or end_page is None:
        return JsonResponse(({'error': 'Missing parameters'}), content_type='application/json')
    _result = get_numbers(
        url,
        page_query_param='page',
        not_found_class='not_found',
        item_link_class="products-i__link",
        store_item_link_class="shop-contact--phones-number",
        item_class="phone",
        first_page=int(first_page),
        end_page=int(end_page)
    )
    print(f'{BColors.OK_GREEN}[+]{BColors.END} Saving data to database')

    _phone_numbers = []
    for item in _result['result']:
        unique_phone_number = list(filter(check_phone_unique, item['phone_numbers']))
        if unique_phone_number:
            phone_number_obj = PhoneNumber(
                phone_number=unique_phone_number[0],
                url=item['url'],
            )
            _phone_numbers.append(phone_number_obj)

    _db_data = PhoneNumber.objects.bulk_create(_phone_numbers)
    print(f'{BColors.OK_GREEN}[+]{BColors.END} Data saved to database')
    return JsonResponse(_result, content_type='application/json', status=200, safe=False)


@csrf_exempt
@require_POST
def get_numbers(request):
    mac_id = request.POST.get('mac_id')
    if MacID.objects.filter(mac_id=mac_id).exists():

        n = PhoneNumber.objects.all()
        d = [
            {"phone":i.phone_number} for i in n
        ]

        return JsonResponse({
            "message":"success",
            "data":d
        }, safe=False)
    return JsonResponse({"message":"error"})