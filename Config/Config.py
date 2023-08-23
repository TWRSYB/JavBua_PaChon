# 爬虫输出目录
OUTPUT_DIR = 'D:/34.Temp/05.JavBus数据爬取/01.TEMP'
PIC_DIR_ACTRESS_AVATAR = f"{OUTPUT_DIR}/images/Actress_avatar"
PIC_DIR_MOVIE_COVER_PIC = f"{OUTPUT_DIR}/images/Movie_cover_pic"
PIC_DIR_MOVIE_GALLERY_PIC = f"{OUTPUT_DIR}/images/Movie_gallery_pic"

# JSON_DATA的存储路径
JSON_DATA_ACTRESS = f"{OUTPUT_DIR}/jsondatas/actress.txt"
JSON_DATA_MOVIE = f"{OUTPUT_DIR}/jsondatas/movie.txt"
JSON_DATA_GENRE = f"{OUTPUT_DIR}/jsondatas/genre.txt"
JSON_DATA_MAKER = f"{OUTPUT_DIR}/jsondatas/maker.txt"
JSON_DATA_LABEL = f"{OUTPUT_DIR}/jsondatas/label.txt"
JSON_DATA_SERIES = f"{OUTPUT_DIR}/jsondatas/series.txt"
JSON_DATA_MAGNET = f"{OUTPUT_DIR}/jsondatas/magnet.txt"

# 请求地址
URL_HOST = 'https://www.javbus.com'
URL_HOST_CN = f'{URL_HOST}'
URL_HOST_JP = f'{URL_HOST}/ja'
URL_HOST_EN = f'{URL_HOST}/en'
URL_HOST_KR = f'{URL_HOST}/ko'
API_PATH_UNCENSORED_ACTRESSES = '/uncensored/actresses'
API_PATH_ACTRESS_MOVIE = '/uncensored/star'
API_PATH_MOVIE = ''

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://www.javbus.com',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',

}
