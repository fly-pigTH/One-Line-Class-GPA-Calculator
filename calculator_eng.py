import pandas as pd
grouped_df = pd.read_excel(
        'Undergraduate_Academic_Record_Query_by_Class.xls'     # File Name
    ).assign(
        Required_or_Elective=lambda x: x['Course_Attribute'].map({"Required": 1, "Limited_Elective": 1, "Free_Elective": 0}),    # Class Property
        Grade_Credits_Req_Elec_Free=lambda x: x['Credits'] * x['Grade_Point_Average'],                    # Grade of a class 
        Grade_Credits_Req_Elec=lambda x: x['Grade_Credits_Req_Elec_Free'] * x['Required_or_Elective'], 
        Credits_Req_Elec_Free=lambda x: x['Credits'] * x['Grade_Point_Average'].notna().astype(int),    # Credit of a class that is validated
        Credits_Req_Elec=lambda x: x['Credits_Req_Elec_Free'] * x['Required_or_Elective']        
    ).groupby(
        'Student_ID'
    ).agg({
        'Name': 'first',            # Information binded with the student ID
        "Teaching_Class": "first",
        'Grade_Credits_Req_Elec': 'sum',      # Grade
        'Grade_Credits_Req_Elec_Free': 'sum', 
        'Credits_Req_Elec': 'sum', 
        "Credits_Req_Elec_Free": 'sum'
    }).assign(
        GPA_Req_Elec=lambda x: x['Grade_Credits_Req_Elec'] / x['Credits_Req_Elec'],      # Calculate GPA
        GPA_Req_Elec_Free=lambda x: x['Grade_Credits_Req_Elec_Free'] / x['Credits_Req_Elec_Free']
    ).reset_index().to_excel('data/GPA_results.xlsx', index=False)