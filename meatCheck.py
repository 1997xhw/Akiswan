import requests


def main():
    try:
        url = "https://swan.akiiita.com/api/meat/check"
        data = {}
        res = requests.post(url=url, data=data)
        print(res.text)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
