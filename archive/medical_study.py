import pandas as pd
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.font_manager as fm # 폰트 관리자

# ==========================================
# ▼ API 키 입력
API_KEY = "YOUR_API_KEY_HERE" 

# ▼ 검색 키워드
SEARCH_KEYWORD = "당뇨" 
# ==========================================

# [핵심] 폰트 파일 위치를 변수로 저장해둡니다.
# 윈도우라면 보통 여기에 있습니다.
FONT_PATH = 'C:/Windows/Fonts/malgun.ttf'

def get_medical_data():
    print(f"🏥 '{SEARCH_KEYWORD}' 키워드로 데이터를 새로 수집합니다...")
    
    try:
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
        
    except Exception as e:
        print(f"❌ API 데이터 수집 중 오류 발생: {e}")
        return pd.DataFrame() 

if __name__ == "__main__":
    try:
        # 1. 폰트 속성 객체 생성 (이걸로 강제 적용합니다)
        if os.path.exists(FONT_PATH):
            my_font = fm.FontProperties(fname=FONT_PATH, size=14)
        else:
            # 맑은 고딕이 없으면 기본 폰트 사용 (맥 등)
            my_font = fm.FontProperties(size=14)

        # 2. 데이터 불러오기
        csv_path = "../medical_final.csv"
        
        if os.path.exists(csv_path):
            print(f"📂 저장된 데이터 파일({csv_path})을 로딩 중...")
            df = pd.read_csv(csv_path)
        else:
            print("📂 저장된 파일이 없어 API로 수집합니다.")
            df = get_medical_data()

        # 3. 그래프 그리기
        if not df.empty:
            count_check = df['Type'].value_counts()
            print(f"\n[데이터 분포 확인]\n{count_check}")

            plt.figure(figsize=(12, 6))
            sns.set_style("whitegrid")

            # 3-1. 조회수 대결
            plt.subplot(1, 2, 1)
            sns.barplot(data=df, x='Type', y='Views', ci=None, palette='Set2')
            
            # [수정 포인트] fontproperties=my_font 를 직접 넣어줍니다!
            plt.title(f'Views: {SEARCH_KEYWORD} (조회수)', fontproperties=my_font)
            plt.ylabel('Views', fontproperties=my_font)

            # 3-2. 만족도 대결
            plt.subplot(1, 2, 2)
            sns.barplot(data=df, x='Type', y='Like_Ratio', ci=None, palette='RdBu')
            
            # [수정 포인트] 여기도 직접 적용!
            plt.title(f'Satisfaction: (좋아요 비율)', fontproperties=my_font)
            plt.ylabel('Like Ratio (%)', fontproperties=my_font)

            plt.tight_layout()
            plt.show()
            print("\n✅ 그래프 생성 완료! 제발 한글이 나왔으면 좋겠네요!")
        else:
            print("\n⚠️ 데이터를 가져오지 못해 그래프를 그릴 수 없습니다.")

    except Exception as e:
        print("\n❌ 실행 중 오류 발생:", e)