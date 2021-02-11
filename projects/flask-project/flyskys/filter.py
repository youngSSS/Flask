# default로 파라미터에 해당하는 형식을 제공한다
# Filter는 출력 형식을 제한해 주는 역할을 한다
def format_datetime(value, fmt='%Y년 %m월 %d일 %H:%M'):
    return value.strftime(fmt)
