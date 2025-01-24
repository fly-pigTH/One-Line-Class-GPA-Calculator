import pandas as pd
gourped_df = pd.read_excel(
        'data/本科生成绩信息查询_按班级.xls'     # File Name
    ).assign(
        必限=lambda x: x['课程属性'].map({"必修": 1, "限选": 1, "任选": 0}),    # Class Property
        学分绩点_必限任=lambda x: x['学分'] * x['绩点成绩'],                    # Grade of a class 
        学分绩点_必限=lambda x: x['学分绩点_必限任'] * x['必限'], 
        学分_必限任=lambda x: x['学分'] * x['绩点成绩'].notna().astype(int),    # Credit of a class that is validated
        学分_必限=lambda x: x['学分_必限任'] * x['必限']        
    ).groupby(
        '学号'
    ).agg({
        '姓名': 'first',            # Information binded with the student ID
        "教学班级": "first",
        '学分绩点_必限': 'sum',      # Grade
        '学分绩点_必限任': 'sum', 
        '学分_必限': 'sum', 
        "学分_必限任": 'sum'
    }).assign(
        GPA_必限=lambda x: x['学分绩点_必限'] / x['学分_必限'],      # 计算GPA
        GPA_必限任=lambda x: x['学分绩点_必限任'] / x['学分_必限任']
    ).reset_index().to_excel('GPA_results.xlsx', index=False)