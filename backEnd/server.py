from flask import Flask
from flask_cors import CORS
import openpyxl

# 创建 Flask 应用
app = Flask(__name__)
# 允许跨域访问
CORS(app)


# 定义根路由处理函数
@app.route('/getData')
def get_data():
    # 表格路径
    excel_path = '../dataSets/2024QS.xlsx'
    workbook = openpyxl.load_workbook(excel_path)
    sheet = workbook.active  # 默认使用第一个工作表，可以根据实际情况修改
    data = []
    for row_num, row in enumerate(sheet.iter_rows(min_row=5, max_row=105, min_col=1, max_col=27, values_only=True),
                                  start=5):
        selected_data = {"rank": row[0], "name": row[2], "country": row[3], "Academic Reputation": row[10],
                         "Employer Reputation": row[12], "Faculty Student": row[14], "Citations per Faculty": row[16],
                         "International Faculty": row[18], "International Students": row[20],
                         "International Research Network": row[22],
                         "Employment Outcomes": row[24], "Sustainability": row[26]}
        data.append(selected_data)
    country = []
    for i in data:
        if i['country'] not in country:
            country.append(i['country'])

    return [data, country]


if __name__ == '__main__':
    app.run()
