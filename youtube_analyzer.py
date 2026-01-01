import pandas as pd
from googleapiclient.discovery import build
from collections import Counter
import os

# 🛠️ 분리한 processor 모듈에서 전처리 함수 가져오기
# 파일명이 반드시 processor.py여야 합니다.
try:
    from processor import clean_text, get_meaningful_words
except ImportError:
    print("❌ 오류: 'processor.py' 파일을 찾을 수 없습니다. 같은 폴더에 있는지 확인해주세요.")

# =========================================================
# ⚙️ [설정] API 키와 검색어
# =========================================================
API_KEY = "YOUR_API_KEY_HERE"  # 본인의 API 키
SEARCH_KEYWORD = "당뇨"
FILE_NAME = "medical_final.csv"

# =========================================================
# 1. 데이터 수집 모듈 (ETL: Extract)
# =========================================================
def get_or_create_data():
    """데이터 파일이 있으면 로드하고, 없으면 유튜브 API로 새로 수집합니다."""
    if os.path.exists(FILE_NAME):
        print(f"✅ 기존 데이터 파일('{FILE_NAME}')을 발견했습니다. 로딩 중...")
        return pd.read_csv(FILE_NAME)
    
    print(f"🚀 데이터 파일이 없습니다. '{SEARCH_KEYWORD}' 관련 데이터를 새로 수집합니다...")
    
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        
        # 조회수 높은 순으로 50개 검색
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
        df.to_csv(FILE_NAME, index=False, encoding='utf-8-sig')
        print(f"💾 데이터 수집 완료! '{FILE_NAME}'로 저장했습니다.")
        return df
    except Exception as e:
        print(f"❌ API 수집 중 오류 발생: {e}")
        return None

# =========================================================
# 2. 데이터 학습 모듈 (Training)
# =========================================================
def train_model(df):
    """일반인 타겟의 고효율 키워드를 학습하여 점수표(모델)를 만듭니다."""
    print("🤖 전처리 엔진을 가동하여 데이터를 학습하는 중...")
    
    target_df = df[df['Type'] == 'General']
    titles = target_df['Title'].tolist()
    
    all_words = []
    # 분석의 핵심을 흐리는 불용어 제외
    stop_words = [SEARCH_KEYWORD, '당뇨병', '에', '이', '가', '은', '는', '방법', '가장', '진짜', '있습니다', '드립니다', '합니다']
    
    for title in titles:
        # processor.py에 정의한 로직으로 의미 있는 단어만 추출
        meaningful_words = get_meaningful_words(title, stop_words)
        all_words.extend(meaningful_words)
    
    # 단어 빈도수 계산
    word_scores = Counter(all_words)
    return word_scores

# =========================================================
# 3. 예측 모듈 (Inference) - 판독 게임 로직
# =========================================================
def predict_score(new_title, model):
    """사용자가 입력한 제목을 학습된 데이터와 비교하여 점수를 매깁니다."""
    # 💡 [중요] 입력받은 제목도 학습 때와 동일한 전처리(clean_text) 과정을 거칩니다.
    cleaned_title = clean_text(new_title)
    words = cleaned_title.split()
    
    total_score = 0
    matched_words = []
    
    for word in words:
        if word in model:
            # 빈도수에 따른 가중치 점수 (1회당 5점)
            score = model[word] * 5
            total_score += score
            matched_words.append(f"{word}(+{score})")
            
    # 숫자 포함 시 시선을 끄는 효과가 크므로 가산점 부여
    if any(char.isdigit() for char in new_title):
        total_score += 10
        matched_words.append("숫자포함(+10)")
    
    # 최종 점수는 100점으로 제한
    final_score = min(total_score, 100)
    
    print(f"\n" + "-"*30)
    print(f"📄 분석 대상: [{new_title}]")
    print(f"🧹 정제 결과: [{cleaned_title}]") # 전처리된 결과 확인용
    
    if matched_words:
        print(f"   👉 흥행 요인: {', '.join(matched_words)}")
    else:
        print("   👉 분석 결과: 인기 키워드와 일치하는 단어가 없습니다.")
        
    print(f"🏆 최종 흥행 지수: {final_score}점")
    print("-"*30)

# =========================================================
# 🚀 메인 실행부
# =========================================================
if __name__ == "__main__":
    try:
        # 1. 데이터 준비
        df = get_or_create_data()
        
        if df is not None:
            # 2. 모델 학습
            ai_model = train_model(df)
            
            print("\n" + "="*45)
            print("💉 MEDICAL CONTENT OPTIMIZER (GAME MODE)")
            print("="*45)
            print("안내: 인기 당뇨 영상 제목을 학습했습니다.")
            print("     당신의 제목은 얼마나 인기가 있을까요?")
            
            # 3. 인터랙티브 게임 모드
            while True:
                user_input = input("\n✍️  제목을 입력하세요 (종료: q): ")
                if user_input.lower() == 'q':
                    print("\n🎮 분석기를 종료합니다. 감사합니다!")
                    break
                
                if not user_input.strip():
                    continue
                    
                predict_score(user_input, ai_model)
            
    except Exception as e:
        print(f"\n❌ 프로그램 실행 오류: {e}")