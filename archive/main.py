import pandas as pd
from googleapiclient.discovery import build

# ==========================================
# ▼ API 키를 다시 입력해주세요 ▼
API_KEY = "YOUR_API_KEY_HERE"
SEARCH_KEYWORD = "생성형 AI"
# ==========================================

def get_youtube_data():
    print(f"🔎 '{SEARCH_KEYWORD}' 데이터 수집 중...")
    
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    # 상위 20개 검색
    search_response = youtube.search().list(
        q=SEARCH_KEYWORD,
        part='id,snippet',
        maxResults=20, 
        type='video',
        order='viewCount'
    ).execute()
    
    video_ids = [item['id']['videoId'] for item in search_response['items']]
    
    # 상세 정보 조회
    video_response = youtube.videos().list(
        part='snippet,statistics',
        id=','.join(video_ids)
    ).execute()
    
    data_list = []
    for item in video_response['items']:
        stats = item['statistics']
        snippet = item['snippet']
        
        data_list.append({
            'Title': snippet['title'],      # 한글 깨짐 방지를 위해 영어 컬럼명 사용
            'Channel': snippet['channelTitle'],
            'Views': int(stats.get('viewCount', 0)),
            'Likes': int(stats.get('likeCount', 0)),
            'Comments': int(stats.get('commentCount', 0)),
            'Date': snippet['publishedAt'][:10]
        })
    
    return pd.DataFrame(data_list)

if __name__ == "__main__":
    try:
        df = get_youtube_data()
        
        # ▼▼▼ 여기가 바뀌었습니다 (Excel -> CSV) ▼▼▼
        # encoding='utf-8-sig'는 한글이 안 깨지게 해주는 마법의 옵션입니다.
        file_name = "youtube_result.csv"
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
        
        print(f"\n✅ 저장 완료! 왼쪽 파일 목록에서 '{file_name}'을 클릭해보세요.")
        
        # 터미널에서도 바로 보이게 출력
        print("\n[수집된 데이터 미리보기]")
        print(df[['Title', 'Views', 'Likes']].head())
        
    except Exception as e:
        print("\n❌ 오류 발생:", e)