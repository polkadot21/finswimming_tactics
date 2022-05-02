import pandas as pd


def _add_wr_with_to_data(df: pd.DataFrame, wr: pd.DataFrame) -> pd.DataFrame:
    for idx, value_1 in enumerate(df['Место']):
        for jdx, value_2 in enumerate(wr['Мировой рекорд в сек']):

            if 'девочки' in value_1:
                value_1 = value_1.replace('девочки', 'женщины')
            elif 'девушки' in value_1:
                value_1 = value_1.replace('девушки', 'женщины')
            elif 'мальчики' in value_1:
                value_1 = value_1.replace('мальчики', 'мужчины')
            elif 'юноши' in value_1:
                value_1 = value_1.replace('юноши', 'мужчины')

            if value_1 == wr["Дистанция"].iloc[jdx]:
                df['Мировой рекорд'].iloc[idx] = value_2

    return df


if __name__ == "__main__":
    df = pd.read_csv('df.csv', index_col=0)
    wr = pd.read_csv('wr.csv', index_col=0)

    df = _add_wr_with_to_data(df, wr)
    print(pd.to_datetime(df['Результат']))
