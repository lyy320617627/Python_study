import pandas as pd
import os
from MySQLUtil import MySQLUtil


class DataUploaded:
    def get_desktop_path(self):
        """获取系统桌面路径并返回"""
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        return desktop_path
    def data_uploaded(self, filepath):
        conn = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        data = pd.read_excel(filepath, keep_default_na=False, index_col=None)
        columns = data.columns
        datalist = data.values.tolist()
        keylist = [
            "document_number", "phone_number", "original_supplier", "supplier", "supplier_type", "sales_date",
            "entry_date", "mnemonic_code", "product", "product_full_name", "scm_material_code", "memory", "version",
            "color", "mode", "product_grade", "brand", "product_category", "quantity", "retail_price", "unit_price",
            "amount", "payment_method", "pool_usage_amount", "cost", "gross_profit", "gross_profit_margin",
            "assessment_cost",
            "assessment_gross_profit", "rebate_amount", "rebate_cost_price", "price_protection_amount", "minimum_price",
            "phone_subsidy_cost", "phone_subsidy_gross_profit", "salesperson", "salesperson2", "sales_position",
            "sales_position2", "product_attribute", "reward", "penalty", "city", "district", "retail_manager",
            "store_type", "store", "warehouse", "retail_serial_number", "customer", "header_remark", "remark",
            "outbound_type", "outbound_method", "sales_type", "marketing_activity_type", "marketing_activity_name",
            "package", "customer_name", "customer_phone", "customer_address", "id_number", "original_order_id",
            "manual_order_number", "modification_date", "created_by", "modified_by", "invoice_status",
            "invoicing_method",
            "tax_inclusive_amount", "invoice_type", "invoice_number", "invoice_batch", "invoice_date",
            "bulk_purchase_batch_number", "pad_order_number", "special_price_sales_order_number",
            "installment_business_contract_number", "procurement_type", "pos", "cash", "alipay", "wechat", "e_voucher",
            "deposit", "telecom_collection", "telecom_points", "third_party_points", "third_party_collection",
            "telecom_unified_cashier", "others", "total_amount", "serial_number_label", "store_code", "province",
            "extra_single_unit_reward", "in_activity_type", "boss_organization_code", "province_code", "belonging_city",
            "city_code", "completion_time", "scm_sales_office", "scm_material_name", "scm_alias", "material_group_name",
            "model_alias", "ordering_channel", "apple_id", "physical_address_code", "is_model_store",
            "is_own_machine_insurance", "is_serial_number_returned", "points_deduction_amount",
            "is_government_enterprise",
            "warehouse_type", "collection", "public_payment", "store_category", "unified_cashier_wechat",
            "unified_cashier_alipay", "unified_cashier_unionpay", "unified_cashier_card", "unified_cashier_instalment",
            "material_group_code", "contract_name", "contract_code", "product_price_range", "retail_agreement_price",
            "product_launch_time", "scm_sales_order_status", "platform_discount", "merchant_discount",
            "contract_collection",
            "jd_home_merchant_shipping_fee", "jd_home_user_shipping_fee", "jd_home_commission", "jd_home_packaging_fee"
        ]
        conn.batchInsert('bs_sale_daily_report', keylist, datalist)
        sql="CALL proc_sale_daily_report();"
        conn.execute(sql)


def get_desktop_path():
    """获取系统桌面路径并返回"""
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    return desktop_path


def get_all_files_in_folder(folder_name):
    """获取指定文件夹下的所有文件"""
    desktop_path = get_desktop_path()
    folder_path = os.path.join(desktop_path, folder_name)

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"指定的文件夹 {folder_name} 不存在。")

    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            all_files.append(os.path.join(root, file))

    return all_files

if __name__ == '__main__':
    dataUploaded = DataUploaded()
    desktop=dataUploaded.get_desktop_path()
    filePath = f"{desktop}\\泛全文件.xlsx"
    print(f"文件的路径为:{filePath}")
    folder_name = "泛全文件下载"  # 替换成实际的文件夹名称
    files = get_all_files_in_folder(folder_name)
    sum=0
    for file in files:
        print(file)
        data=pd.read_excel(file)
        data=data.values.tolist()
        print(f"文件{file}中的数据长度为:{len(data)}")
        sum=sum+len(data)
        dataUploaded.data_uploaded(filepath=file)
    print(f"文件的总长度为{sum}")
