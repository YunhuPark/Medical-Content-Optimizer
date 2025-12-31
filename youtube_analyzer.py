import pandas as pd
from googleapiclient.discovery import build
import re
from collections import Counter
import os

# =========================================================
# ⚙️ [설정] API 키와 검색어
# =========================================================
API_KEY = "YOUR_API_KEY_HERE"  # <-- 본인 키 입력
SEARCH_KEYWORD = "당뇨"
FILE_NAME = "medical_final.csv"

# =========================================================
# 1. 데이터 수집 모듈 (ETL: Extract)
# 파일이 없으면 유튜브에서 긁어오고, 있으면 건너뜁니다.
# =========================================================
def get_or_create_data():
    # 파일이 이미 있는지 확인
    if os.path.exists(FILE_NAME):
        print(f"✅ 기존 데이터 파일('{FILE_NAME}')을 발견했습니다. 로딩 중...")
        return pd.read_csv(FILE_NAME)
    
    print(f"🚀 데이터 파일이 없습니다. '{SEARCH_KEYWORD}' 관련 데이터를 새로 수집합니다...")
    
    # 유튜브 API 연결
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    # 데이터 수집 (50개)
    search_response = youtube.search().list(
        q=SEARCH_KEYWORD, part='id,snippet', maxResults=50, 
        type='video', order='viewCount'
    ).execute()
    
    video_ids = [item['id']['videoId'] for item in search_response['items']]
    video_response = youtube.videos().list(
        part='snippet,statistics', id=','.join(video_ids)
    ).execute()
    
    data_list = []
    doctor_keywords = ['의사', '닥터', 'dr', '병원', '약사', '한의사', '전문의', '교수', '의원', 'md']

    for item in video_response['items']:
        channel_name = item['snippet']['channelTitle']
        # 전문가 vs 일반인 분류
        is_expert = "General"
        for key in doctor_keywords:
            if key in channel_name.lower(): 
                is_expert = "Medical Pro"
                break
        
        data_list.append({
            'Title': item['snippet']['title'],
            'Channel': channel_name,
            'Type': is_expert
        })
    
    df = pd.DataFrame(data_list)
    # CSV 파일로 저장 (한글 깨짐 방지 utf-8-sig)
    df.to_csv(FILE_NAME, index=False, encoding='utf-8-sig')
    print(f"💾 데이터 수집 완료! '{FILE_NAME}'로 저장했습니다.")
    
    return df

# =========================================================
# 2. 데이터 학습 모듈 (Training)
# 일반인 유튜버들의 고효율 단어를 학습합니다.
# =========================================================
def train_model(df):
    print("🤖 데이터를 학습하여 점수표를 만드는 중...")
    
    # 일반인(General) 영상의 제목만 추출
    target_df = df[df['Type'] == 'General']
    titles = target_df['Title'].tolist()
    
    # 텍스트 전처리 및 단어 추출
    all_words = []
    stop_words = [SEARCH_KEYWORD, '당뇨병', '에', '이', '가', '은', '는', '방법', '가장', '진짜']
    
    for title in titles:
        clean_text = re.sub(r'[^\w\s]', '', title) # 특수문자 제거
        words = clean_text.split()
        # 의미 있는 단어만 필터링
        meaningful_words = [w for w in words if w not in stop_words and len(w) > 1]
        all_words.extend(meaningful_words)
    
    # 빈도수 기반 점수표 생성
    word_scores = Counter(all_words)
    return word_scores

# =========================================================
# 3. 예측 모듈 (Inference)
# =========================================================
def predict_score(new_title, model):
    clean_title = re.sub(r'[^\w\s]', '', new_title)
    words = clean_title.split()
    
    total_score = 0
    matched_words = []
    
    for word in words:
        if word in model:
            # 빈도수 1회당 5점씩 부여 (가중치)
            score = model[word] * 5
            total_score += score
            matched_words.append(f"{word}(+{score})")
            
    # 숫자 포함 시 가산점
    if any(char.isdigit() for char in new_title):
        total_score += 10
        matched_words.append("숫자포함(+10)")
    
    # 100점 만점으로 제한
    final_score = min(total_score, 100)
    
    # 리포트 출력
    print(f"\n📄 입력 제목: [{new_title}]")
    if matched_words:
        print(f"   👉 점수 요인: {', '.join(matched_words)}")
    else:
        print("   👉 점수 요인: 없음 (너무 평범합니다)")
    print(f"   🏆 최종 점수: {final_score}점")

# =========================================================
# 🚀 메인 실행
# =========================================================
if __name__ == "__main__":
    try:
        # 1. 데이터 준비
        df = get_or_create_data()
        
        # 2. 모델 학습
        ai_model = train_model(df)
        
        print("\n" + "="*40)
        print("💉 당뇨 유튜브 제목 AI 판독기")
        print("="*40)
        
        # 3. 사용자 테스트
        while True:
            user_input = input("\n✍️ 제목을 입력하세요 (종료: q): ")
            if user_input.lower() == 'q':
                break
            predict_score(user_input, ai_model)
            
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("API 키를 확인하거나 인터넷 연결을 확인해주세요.")