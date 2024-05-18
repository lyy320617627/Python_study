import pandas as pd
if __name__ == '__main__':
    excel_list = ['C:\\Users\\ly320\\Desktop\\接单.xlsx', 'C:\\Users\\ly320\\Desktop\\包装.xlsx',
                  'C:\\Users\\ly320\\Desktop\\复核.xlsx', 'C:\\Users\\ly320\\Desktop\\拣配.xlsx',
                  'C:\\Users\\ly320\\Desktop\\发货.xlsx']
    num_rows_list = []
    for i in excel_list:
            data = pd.read_excel(i)
            num_rows = data.shape[0]
            num_rows_list.append(num_rows)
            if num_rows>0:
                excel_list.append(i)
            # print(f"行数：{num_rows}")
    print(excel_list)
    print(num_rows_list)

    # for i in excel_list:
    #         my_tuple=i.split('.')
    #         print(f"分割之后的数组是：{my_tuple}")
    #         program_name=my_tuple[0][-2:]
    #         print(program_name)
    #         # target_list=conn2.get_warn_or_timeout('bs_rtime_oper_eff_warn',program_name)
    #         # print(f"warn_sitution={target_list[0][0]}")
    #         # print(f"delay_time={target_list[0][1]}")
    #         #
    #         # print(f"{program_name} 环节 ，超{target_list[0][1]}时未处理:{target_list[0][0]}请及时处理")