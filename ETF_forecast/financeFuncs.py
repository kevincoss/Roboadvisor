import numpy as np
import pandas as pd

def feature_engineering(ticker_df, bm_df, close_px_type='Adj Close', n_days=1):
    """
    파생변수 생성 함수
    """
    # 인덱스를 날짜로 사용하는 경우, 별도로 'Date' 컬럼을 생성할 필요 없음
    # ticker_df의 인덱스가 날짜임을 가정

    # 수익률 계산
    price_diff = np.log(ticker_df[close_px_type]).diff(n_days) - np.log(bm_df[close_px_type]).diff(n_days)

    # 이동평균선과 변동성 지표 계산
    ma_dict = {f'ma_{n}': price_diff.rolling(n).mean() for n in [10, 20, 30, 40, 50, 60, 90, 120, 180, 255]}
    vol_ma_dict = {f'vol_ma_{n}': price_diff.rolling(n).std() for n in [10, 20, 30, 40, 50, 60, 90, 120, 180, 255]}
    # vol_diff_dict: 개별 종목(지수)의 최근 거래량(Volume)
    vol_diff_dict = {f'vol_diff_{recent_n}_by_500': ticker_df['Volume'].rolling(recent_n).mean() / ticker_df['Volume'].rolling(500).mean()
                for recent_n in [10, 20, 30, 40, 50, 60, 90, 120, 180, 255]}
    # vol_diff_by_bm_dict: 벤치마크 대비 개별 종목(지수)의 이동평균 거래량(Volume)
    vol_diff_by_bm_dict = {f'vol_diff_by_bm_{n}': ticker_df['Volume'].rolling(n).mean() / bm_df['Volume'].rolling(n).mean()
                        for n in [5, 10, 20, 60, 120, 240]}

    # 계산된 특성을 기존 데이터프레임에 추가
    features = pd.DataFrame({
        'price_diff': price_diff,
        'volume': ticker_df['Volume'],
        'high_low_gap': ticker_df['High'] - ticker_df['Low'],
        'vol_diff_by_bm': ticker_df['Volume'] / bm_df['Volume'] # vol_diff_by_bm: 벤치마크 대비 개별 종목(지수)의 거래량(Volume)
    }, index=ticker_df.index)  # 인덱스 지정

    for k, v in {**ma_dict, **vol_ma_dict, **vol_diff_dict, **vol_diff_by_bm_dict}.items():
        features[k] = v
    
    return features
        


def cal_return(buy_price, sell_price, dividend=0):
    """
    주식 수익률 계산 함수

    :param buy_price: 주식 구매가
    :param sell_price: 주식 판매가
    :param dividend: 받은 배당금 (기본값은 0)
    :return: 수익률 (%)
    """
    # 수익률 계산
    return_rate = ((sell_price + dividend - buy_price) / buy_price) * 100
    
    return return_rate
