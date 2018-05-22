import argparse
import os
import sys
import inspect
import validators
import requests


def url_validation(page):
    if not validators.url(page):
        page_error = "%r please provide a valid url. Sample: 'https://apiary.docs.apiary.io'" % page
        raise argparse.ArgumentTypeError(page_error)
    return page


def file_validation(param):
    base, ext = os.path.splitext(param)
    if ext.lower() != '.json':
        file_error = "%r file is not json file. Sample: '<file>.json'" % param
        raise argparse.ArgumentTypeError(file_error)
    return param


parser = argparse.ArgumentParser(description='Process API')
parser.add_argument('-u', '--url', required=True,
                    type=url_validation,
                    help='Url to GET or POST to API')
parser.add_argument('-g', '--get', action='store_true',
                    help='Url to retrieve from the API')
parser.add_argument('-p', '--post',
                    type=file_validation,
                    help='POST file to the API')


def handle_get(html_link):
    return requests.get(html_link)


def handle_post(page, file_to_send):
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
