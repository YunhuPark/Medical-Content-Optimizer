import pandas as pd
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================
# ▼ API 키 입력 (본인 키로 꼭 바꿔주세요!)
API_KEY = "YOUR_API_KEY_HERE"

# ▼ [핵심 수정] 의사가 많이 나오는 키워드로 변경!
# 추천: "당뇨", "임플란트", "허리디스크", "우울증"
SEARCH_KEYWORD = "당뇨" 
# ==========================================

def get_medical_data():
    print(f"🏥 '{SEARCH_KEYWORD}' 키워드로 의사 vs 일반인 다시 붙어봅니다!")
    
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    # 영상 50개 수집
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
    
    # 전문가 키워드 확장 (영어 대소문자 구분 없이 찾기 위해 로직 개선)
    doctor_keywords = ['의사', '닥터', 'dr', '병원', '약사', '한의사', '전문의', '교수', '의원', 'clinic', 'md']

    for item in video_response['items']:
        stats = item['statistics']
        snippet = item['snippet']
        channel_name = snippet['channelTitle']
        
        # 전문가 여부 판별 (소문자로 바꿔서 비교)
        is_expert = "General" # 기본값: 일반인
        for key in doctor_keywords:
            if key in channel_name.lower(): 
                is_expert = "Medical Pro" # 전문가 발견!
                break
        
        views = int(stats.get('viewCount', 0))
        likes = int(stats.get('likeCount', 0))
        
        like_ratio = (likes / views * 100) if views > 0 else 0
        
        data_list.append({
            'Title': snippet['title'],
            'Channel': channel_name,
            'Type': is_expert,
            'Views': views,
            'Like_Ratio': like_ratio
        })
    
    return pd.DataFrame(data_list)

if __name__ == "__main__":
    try:
        df = get_medical_data()
        
        # 데이터가 너무 한쪽으로 쏠렸는지 확인
        count_check = df['Type'].value_counts()
        print(f"\n[데이터 분포 확인]\n{count_check}")

        # 그래프 그리기
        plt.figure(figsize=(12, 5))
        sns.set_style("whitegrid") # 배경 깔끔하게

        # 1. 조회수 대결
        plt.subplot(1, 2, 1)
        sns.barplot(data=df, x='Type', y='Views', errorbar=None, palette='Set2')
        plt.title(f'Views: {SEARCH_KEYWORD}', fontsize=14)

        # 2. 만족도 대결
        plt.subplot(1, 2, 2)
        sns.barplot(data=df, x='Type', y='Like_Ratio', errorbar=None, palette='Set2')
        plt.title(f'Satisfaction (Like Ratio)', fontsize=14)

        plt.tight_layout()
        plt.show()
        print("\n✅ 그래프가 떴습니다! 이번엔 두 막대가 다 나오나요?")

    except Exception as e:
        print("\n❌ 오류 발생:", e)