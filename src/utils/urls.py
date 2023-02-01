def get_url_with_page(page, url):
    if url.find('?') == -1:
        return f'{url}?currentpage={page}'
    else:
        return f'{url}&currentpage={page}'
