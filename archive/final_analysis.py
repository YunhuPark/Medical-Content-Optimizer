import pandas as pd
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import platform

# ==========================================
# ▼ API 키를 입력하세요 (꼭 바꿔주세요!)
API_KEY = "YOUR_API_KEY_HERE"
SEARCH_KEYWORD = "당뇨" 
# ==========================================

def run_full_analysis():
    # ---------------------------------------------------------
    # 1단계: 데이터 수집 (아까 그 '진검승부' 코드)
    # ---------------------------------------------------------
    print(f"🚀 '{SEARCH_KEYWORD}' 관련 최신 데이터를 수집하고 있습니다...")
    
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    search_response = youtube.search().list(
        q=SEARCH_KEYWORD,
        part='id,snippet',
        maxResults=50, 
        type='video',
        order='viewCount'
    ).execute()
    
    video_ids = [item['id']['videoId'] for item in search_response['items']]
    
    video_response = youtube.videos().list(
        part='snippet,statistics',
        id=','.join(video_ids)
    ).execute()
    
    data_list = []
    doctor_keywords = ['의사', '닥터', 'dr', '병원', '약사', '한의사', '전문의', '교수', '의원', 'clinic', 'md']

    for item in video_response['items']:
        stats = item['statistics']
        snippet = item['snippet']
        channel_name = snippet['channelTitle']
        
        is_expert = "General"
        for key in doctor_keywords:
            if key in channel_name.lower(): 
                is_expert = "Medical Pro"
                break
        
        data_list.append({
            'Title': snippet['title'],
            'Channel': channel_name,
            'Type': is_expert
        })
    
    df = pd.DataFrame(data_list)
    
    # [중요] 이번에는 데이터를 꼭 저장합니다!
    df.to_csv('medical_final.csv', index=False, encoding='utf-8-sig')
    print("✅ 데이터 수집 및 저장 완료 (medical_final.csv)")

    # ---------------------------------------------------------
    # 2단계: 키워드 분석 (일반인 유튜버의 비법 단어 찾기)
    # ---------------------------------------------------------
    print("🔍 일반인 유튜버들의 제목을 분석 중입니다...")
    
    # 'General' 데이터만 뽑기
    target_df = df[df['Type'] == 'General']
    
    if len(target_df) == 0:
        print("앗! 일반인 영상이 하나도 없네요. 키워드를 바꿔보세요.")
        return

    # 텍스트 청소 및 단어 추출
    titles = target_df['Title'].tolist()
    all_text = " ".join(titles)
    clean_text = re.sub(r'[^\w\s]', '', all_text) # 특수문자 제거
    words = clean_text.split()

    # 불용어(검색어 등) 제거
    stop_words = [SEARCH_KEYWORD, '당뇨병', '에', '이', '가', '은', '는', '을', '를', '의', '하는', '있는', '방법', '가장', '진짜']
    meaningful_words = [w for w in words if w not in stop_words and len(w) > 1]

    # 빈도수 계산
    word_counts = Counter(meaningful_words)
    top_words = word_counts.most_common(15)
    word_df = pd.DataFrame(top_words, columns=['Word', 'Count'])

    # ---------------------------------------------------------
    # 3단계: 그래프 그리기
    # ---------------------------------------------------------
    # 폰트 설정
    system_name = platform.system()
    if system_name == 'Windows':
        plt.rc('font', family='Malgun Gothic')
    elif system_name == 'Darwin':
        plt.rc('font', family='AppleGothic')
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=word_df, y='Word', x='Count', palette='viridis')
    plt.title(f"'{SEARCH_KEYWORD}' 일반인 영상 조회수 치트키 단어 TOP 15", fontsize=15)
    plt.xlabel('등장 횟수')
    
    print("\n🎉 분석 성공! 그래프를 확인하세요.")
    plt.show()

# 실행
if __name__ == "__main__":
    try:
        run_full_analysis()
    except Exception as e:
        print("\n❌ 오류 발생:", e)