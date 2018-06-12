# Exception 클래스를 상속한 클래스를 만든다
class CustomException(Exception):
    # 생성할때 value 값을 입력 받는다.
    def __init__(self, value):
        self.value = value

    # 생성할때 받은 value 값을 확인 한다.
    def __str__(self):
        return self.value

    # 예외를 발생하는 함수
    def raise_exception(self, err_msg):
        raise CustomException(err_msg)