import re

from lxml import html

from consts import xpath


def _get_text(tree, xpath_query: str):
    return tree.xpath(xpath_query)[0].text


def get_description(tree):
    description = tree.xpath(xpath.description)[0]
    description = ''.join(description.itertext())
    return description.replace('\xa0', '').replace('\r', '').replace('\n\n', '\n')


def get_description_title(tree):
    return _get_text(tree, xpath.description_title)


def get_params(tree):
    params = tree.xpath(xpath.params)
    return {i.xpath(f'./div[1]')[0].text: i.xpath(f'./div[2]')[0].text for i in params}


def get_href(tree):
    href = tree.xpath(xpath.href)
    return f'https://www.truckscout24.de{href[0].attrib.get("href")}'


def get_images(tree):
    image_urls = tree.xpath(f'{xpath.first_item}//img')
    image_urls = [i.attrib.get('data-src') for i in image_urls if i.attrib.get('data-src') is not None]
    return image_urls[:3]


def get_title(tree):
    return _get_text(tree, xpath.title)


def _get_number(tree, xpath_query):
    value = _get_text(tree, xpath_query)
    return int(''.join(re.findall(r'\d', value)))


def get_price(tree):
    return _get_number(tree, xpath.price)


def get_mileage(tree):
    return _get_number(tree, xpath.mileage)


def get_power(dict_columns):
    power = dict_columns.get('Leistung')
    power = re.findall(r'^\d+ kW', power)[0] if power else ''
    power = power.split(' ')[0]
    return int(power) if len(power) else 0


def get_color(dict_columns):
    value = dict_columns.get('Farbe')
    return value if value else ''


def _get_value(tree, xpath_query):
    value = tree.xpath(xpath_query)
    if len(value):
        value = value[0].attrib.get('value')
        if value:
            return value
        else:
            return ''
    else:
        return ''


def get_count_vehicles_params(tree):
    vehicle_type_id = _get_value(tree, xpath.vehicle_type_id_filter)
    substructure_id = _get_value(tree, xpath.substructure_id_filter)
    make_id = _get_value(tree, xpath.make_id_filter)
    country_id = _get_value(tree, xpath.country_id_filter)
    price_type = _get_value(tree, xpath.price_type_filter)
    model = _get_value(tree, xpath.model_filter)
    price_from = _get_value(tree, xpath.price_from_filter)
    price_to = _get_value(tree, xpath.price_to_filter)
    request_verification_token = _get_value(tree, xpath.request_verification_token_filter)

    return {
        'vehicleTypeId': vehicle_type_id,
        'substructureId': substructure_id,
        'makeId': make_id,
        'countryId': country_id,
        'priceType': price_type,
        'model': model,
        'priceFrom': price_from,
        'priceTo': price_to,
        '__RequestVerificationToken': request_verification_token,
        'accidented': '-1'
    }


def get_tree(text: str):
    return html.fromstring(text, parser=html.HTMLParser(encoding='UTF-8'))
