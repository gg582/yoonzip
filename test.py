import os
import pyzipper
from zipfile import ZipInfo
import time

# 설정
filename_kr = "테스트파일.txt"
ascii_password = b"test1234"
zip_filename = "test_euc-kr_aes_ascii_password.zip"

# 테스트용 한글 파일 생성
with open(filename_kr, "w", encoding="utf-8") as f:
    f.write("한글 파일 이름 + AES 암호화 테스트입니다.")

# 원본 파일 데이터 읽기
with open(filename_kr, "rb") as f:
    file_data = f.read()

# ZipInfo 객체 생성 및 EUC-KR 파일명 설정
zip_info = ZipInfo()
zip_info.date_time = time.localtime(time.time())[:6]
zip_info.compress_type = pyzipper.ZIP_DEFLATED
zip_info.flag_bits = 0  # UTF-8 플래그 비활성화

# 파일명 EUC-KR 인코딩 후 설정

