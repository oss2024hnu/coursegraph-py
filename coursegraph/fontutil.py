# 한글 폰트 정보를 가져오는 모듈
# 제발 ttf 파일 path를 하드코딩하지 말 것!!!

def get_system_font():
    system = platform.system()
    if system == 'Windows':
        # Windows의 경우, malgun 폰트 사용
        font_paths = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        malgun_fonts = [font for font in font_paths if 'malgun.ttf' in font.lower()]
        if malgun_fonts:
            return malgun_fonts
        else:
            print("Malgun 폰트를 찾을 수 없습니다.", file=sys.stderr)
    elif system == 'Darwin':
        # macOS의 경우, AppleGothic 폰트 사용(MacOS의 경우 ttf 가 아닌 otf를 사용하는 경우가 존재하기에 ttf파일이 없을시 otf파일을 검색)
        font_paths = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        apple_gothic_fonts = [font for font in font_paths if 'AppleGothic.ttf' in font.lower()]
        if apple_gothic_fonts:
            return applegothic_fonts_ttf
        else:
            # ttf 폰트가 없을 경우 otf 폰트로 다시 시도
            font_paths_otf = font_manager.findSystemFonts(fontpaths=None, fontext='otf')
            apple_gothic_fonts_otf = [font for font in font_paths_otf if 'AppleGothic.otf' in font.lower()]
            if apple_gothic_fonts_otf:
                return applegothic_fonts_otf
            else:
                print("AppleGothic 폰트를 찾을 수 없습니다.", file=sys.stderr)
    else:
        # 리눅스 및 기타 OS의 경우, NanumGothic 폰트 사용
        font_paths = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        nanum_gothic_fonts = [font for font in font_paths if 'NanumGothic.ttf' in font.lower()]
        if nanum_gothic_fonts:
            return nanumgothic_fonts
        else:
            print("NanumGothic 폰트를 찾을 수 없습니다.", file=sys.stderr)
