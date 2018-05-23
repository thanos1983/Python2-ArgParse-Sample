import argparse
import inspect
import os

import requests
import validators


def url_validation(page):
    """
    The function validates the page (url) and raises an error in case of not valid url.
    :param page: HTML page to validate
    :return: the same HTML to be used
    """
    if not validators.url(page):
        page_error = "%r please provide a valid url. Sample: 'https://apiary.docs.apiary.io'" % page
        raise argparse.ArgumentTypeError(page_error)
    return page


def file_validation(param):
    """
    Check user file input for the extension to check if it is valid.
    :param param: file input
    :return: return the name of the file if is passing the validation
    """
    base, ext = os.path.splitext(param)
    if ext.lower() != '.json':
        file_error = "%r file is not json file. Sample: '<file>.json'" % param
        raise argparse.ArgumentTypeError(file_error)
    return param


parser = argparse.ArgumentParser(description='Process API')
# url input -u [html] page
parser.add_argument('-u', '--url', required=True,
                    type=url_validation,
                    help='Url to GET or POST to API')
# get input -g [without flag]
parser.add_argument('-g', '--get', action='store_true',
                    help='Url to retrieve from the API')
# post input -p [file]
parser.add_argument('-p', '--post',
                    type=file_validation,
                    help='POST file to the API')


def handle_get(html_link):
    """
    Get the page based on url REST (GET)
    :param html_link: page to fetch
    :return: data fetched
    """
    return requests.get(html_link)


def handle_post(page, file_to_send):
    """
    Send json request REST (POST). The function is reading the file and sending in binary format the json data.
    :param page: url to send the POST request
    :param file_to_send: JSON file containing the json data
    :return: the response of the end point
    """
    path = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), file_to_send)
    headers = {'Authorization': 'Token e61c421a7d9d1de7fd7249b8bdb185f7',
               'Accept': 'application/json',
               'Content-Type': 'application/json'}

    return requests.post(page,
                         data=open(path, 'rb'), headers=headers)


if __name__ == '__main__':
    args = parser.parse_args()

    if args.url:
        if args.get:
            request = handle_get(args.url)
            print(request.content)
        elif args.post:
            post_return = handle_post(args.url, args.post)
            print(post_return.content)
        else:
            param_error = "Please provide a valid url. Sample: '-u https://apiary.docs.apiary.io' -g or -p [FILE]"
            print(param_error)
            parser.print_help()
