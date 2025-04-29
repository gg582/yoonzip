KorZip - ZIP 압축 및 해제 프로그램

KorZip은 간단하고 사용하기 쉬운 ZIP 압축 및 해제 프로그램입니다. 명령줄 (CLI) 인터페이스와 그래픽 사용자 인터페이스 (GUI)를 모두 제공하며, 특히 한국어 환경에서 흔히 발생하는 파일명 인코딩 문제 (euc-kr)를 자동으로 처리하려고 시도합니다.
주요 기능

    CLI (명령줄 인터페이스) 지원: 터미널에서 간단한 명령어로 ZIP 파일을 압축 해제할 수 있습니다. 여러 개의 ZIP 파일을 한 번에 처리할 수 있습니다.
    GUI (그래픽 사용자 인터페이스) 지원:
        초기 선택 창: "압축 해제" 또는 "압축" 기능을 선택할 수 있는 직관적인 초기 창을 제공합니다.
        압축 해제 GUI: ZIP 파일을 선택하고 압축을 풀 폴더를 지정할 수 있습니다. 여러 개의 ZIP 파일을 GUI에서 선택하여 일괄 압축 해제할 수 있습니다.
        압축 GUI: 압축할 파일 또는 폴더를 선택하고, ZIP 파일을 저장할 위치를 지정할 수 있습니다.
    파일명 인코딩 처리: ZIP 파일 내의 파일명이 cp437로 인코딩된 후 euc-kr 또는 utf-8로 디코딩을 시도하여 한국어 파일명을 올바르게 처리합니다.
    멀티프로세싱 지원 (압축 해제 GUI): 여러 개의 ZIP 파일을 압축 해제할 때 멀티프로세싱을 사용하여 작업 속도를 향상시킵니다.
    압축 해제 폴더 자동 생성: 지정된 압축 해제 경로가 존재하지 않으면 자동으로 생성합니다.
    오류 처리: 잘못된 ZIP 파일 형식, 파일 없음 등의 오류 상황에 대한 메시지를 제공합니다.

설치 및 실행

    필수 의존성 설치 (GUI 모드): GUI 모드를 사용하려면 GTK+ 3 라이브러리가 설치되어 있어야 합니다.

    Debian/Ubuntu 기반:

    sudo apt-get update
    sudo apt-get install python3-gi gir1.2-gtk-3.0

    Fedora/CentOS/RHEL 기반:

    sudo dnf install python3-gobject gtk3

    다른 운영체제의 경우 해당 패키지 관리자를 사용하여 GTK+ 3 관련 패키지를 설치하세요.

    스크립트 다운로드: 이 Python 스크립트 (korzip.py 등의 이름으로 저장)를 다운로드합니다.

    실행:

        GUI 모드: 터미널에서 스크립트가 있는 디렉토리로 이동한 후 다음 명령어를 실행합니다.

        python korzip.py --gui

        초기 창이 나타나면 "압축 해제" 또는 "압축" 버튼을 클릭하여 원하는 기능을 선택합니다. 각 기능에 맞는 GUI가 나타납니다.

        CLI 모드: 터미널에서 스크립트가 있는 디렉토리로 이동한 후 다음 명령어를 실행합니다.

        python korzip.py <ZIP_파일1> [<ZIP_파일2> ...] <대상_폴더>

        <ZIP_파일1>, <ZIP_파일2> 등에는 압축 해제할 ZIP 파일의 경로를, <대상_폴더>에는 압축을 풀 폴더의 경로를 지정합니다. 여러 개의 ZIP 파일을 공백으로 구분하여 지정할 수 있습니다.

        예시:

        python korzip.py archive1.zip data.zip output

        archive1.zip과 data.zip 파일의 내용이 output 폴더에 압축 해제됩니다.

데스크톱 바로가기 (GUI 모드)

GUI 모드를 더 편리하게 실행하기 위해 데스크톱 바로가기 파일 (.desktop 파일)을 만들 수 있습니다.

    텍스트 편집기를 열고 다음 내용을 입력합니다.
    Ini, TOML

    [Desktop Entry]
    Name=KorZip
    Exec=python3 /path/to/your/script/korzip.py --gui
    Type=Application
    Comment=KorZip GUI 실행
    Icon=application-x-archive
    Categories=Utility;Archiving;

        /path/to/your/script/korzip.py 부분을 실제 스크립트 파일의 절대 경로로 수정하세요.
        Icon은 시스템 테마에 따라 압축 파일 아이콘으로 표시됩니다. 필요에 따라 다른 아이콘 파일 경로를 지정할 수 있습니다.

    작성한 파일을 korzip.desktop과 같은 이름으로 저장합니다.

    저장한 .desktop 파일을 ~/.local/share/applications/ 또는 /usr/share/applications/ 디렉토리로 복사합니다.

    터미널에서 다음 명령어를 실행하여 데스크톱 아이콘 캐시를 업데이트합니다.

    sudo update-desktop-database

    또는

    update-desktop-database ~/.local/share/applications/

이제 애플리케이션 메뉴 등에서 KorZip 아이콘을 통해 GUI 모드를 실행하면 초기 선택 창이 나타납니다.
주의사항

    이 스크립트는 기본적인 ZIP 압축 및 해제 기능만을 제공하며, 암호화된 ZIP 파일이나 다른 압축 형식은 지원하지 않습니다.
    파일명 인코딩 자동 감지는 완벽하지 않을 수 있으며, 드물게 파일명이 깨져 보일 수 있습니다.

기여

버그 보고 및 기능 제안은 언제나 환영합니다.
