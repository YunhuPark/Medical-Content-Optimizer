import re
import pandas as pd

def clean_text(text):
    """
    유튜브 제목의 특수문자, 태그, 해시태그를 제거하여 정제합니다.
    """
    if not isinstance(text, str):
        return ""
    
    # 1. 대괄호, 소괄호 및 그 안의 내용 제거 (예: [ENG SUB], (feat) 등)
    text = re.sub(r'\[.*?\]|\(.*?\)', '', text)
    
    # 2. 이모지 및 특수문자 제거 (한글, 영문, 숫자만 남김)
    text = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', text)
    
    # 3. 해시태그 제거
    text = re.sub(r'#\w+', '', text)
    
    # 4. 불필요한 공백 제거 및 소문자화
    text = " ".join(text.split())
    
    return text.lower()

def get_meaningful_words(title, stop_words):
    """
    분석기에서 사용하는 함수: 텍스트를 정제하고 의미 있는 단어 리스트를 반환합니다.
    """
    cleaned = clean_text(title)
    words = cleaned.split()
    # 불용어 제외 및 2글자 이상 단어만 추출
    return [w for w in words if w not in stop_words and len(w) > 1]

def preprocess_data(file_path):
    """
    CSV 파일 전체를 한 번에 전처리하여 저장할 때 사용하는 함수입니다.
    """
    df = pd.read_csv(file_path)
    df_clean = df.copy()
    
    # 제목(Title) 컬럼 전처리 (첫 번째 컬럼 기준)
    title_col = df_clean.columns[0] 
    df_clean[title_col] = df_clean[title_col].apply(clean_text)
    
    # 채널명(Channel) 공백 제거 (두 번째 컬럼 기준)
    channel_col = df_clean.columns[1]
    df_clean[channel_col] = df_clean[channel_col].str.strip()
    
    return df_clean