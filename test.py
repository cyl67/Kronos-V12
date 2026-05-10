import pandas as pd
from model import Kronos, KronosTokenizer, KronosPredictor

# 加载 tokenizer
tokenizer = KronosTokenizer.from_pretrained(
    "NeoQuasar/Kronos-Tokenizer-base"
)

# 加载模型
model = Kronos.from_pretrained(
    "NeoQuasar/Kronos-mini"
)

# 创建预测器
predictor = KronosPredictor(model, tokenizer)

# 读取数据
df = pd.read_csv("./data/600033_5min.csv")

# 时间格式转换
df['timestamps'] = pd.to_datetime(df['timestamps'])

# 参数
lookback = 400
pred_len = 120

# 输入数据
x_df = df.loc[
    :lookback-1,
    ['open', 'high', 'low', 'close', 'volume', 'amount']
]

# 历史时间
x_timestamp = df.loc[:lookback-1, 'timestamps']

# 未来时间
y_timestamp = df.loc[
    lookback:lookback+pred_len-1,
    'timestamps'
]

# 预测
pred_df = predictor.predict(
    df=x_df,
    x_timestamp=x_timestamp,
    y_timestamp=y_timestamp,
    pred_len=pred_len
)

print(pred_df)