import zipfile

filename_kr = "한글이름파일.txt"
zip_filename = "test_win_compatible_euckr.zip"
password = "test1234"

# 테스트용 파일 생성
with open(filename_kr, "w", encoding="utf-8") as f:
    f.write("Windows 기본 압축기와 호환되는 EUC-KR + ZipCrypto 테스트입니다.")

# 파일 내용 읽기
with open(filename_kr, "rb") as f:
    data = f.read()

# zipfile 모듈은 파일명을 str로 받지만, EUC-KR을 쓸 수 있게 flag_bits=0으로 설정
info = zipfile.ZipInfo(filename_kr.encode('euc-kr').decode('latin1'))
info.flag_bits = 0  # UTF-8 비활성화
info.compress_type = zipfile.ZIP_DEFLATED

with zipfile.ZipFile(zip_filename, 'w') as zf:
    zf.setpassword(password.encode('utf-8'))
    zf.writestr(info, data)

print("Windows 호환 ZIP 파일 생성 완료:", zip_filename)

