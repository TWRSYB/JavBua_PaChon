

print('CREATE TABLE xxx (')

# out_attributes = [attr for attr in dir(MyClass) if not callable(getattr(MyClass, attr)) and attr != "__init__" and not attr.startswith("__")]

out_attributes = """

"""

init_attributes = """
        self.id_fanhao = id_fanhao
        self.id_hash_code = id_hash_code
        self.nm_resources = nm_resources
        self.lj_magnet = lj_magnet
        self.size = size
        self.update_date = update_date
"""

out_attribute_list = out_attributes.splitlines()

out_attribute_list = [(x.split(":")[0].split("=")[0].strip(), x.split('#')[-1].strip() if '#' in x else '') for x in
                      out_attribute_list if x.strip() != ""]

init_attribute_list = init_attributes.splitlines()

init_attribute_list = [
    (x.split(":")[0].split("=")[0].replace('self.', '').strip(), x.split('#')[-1].strip() if '#' in x else '') for x in
    init_attribute_list if x.strip().startswith('self.')]

attribute_list = init_attribute_list + [x for x in out_attribute_list if
                                        x[0] not in [x[0] for x in init_attribute_list]]

for attribute in attribute_list:
    t_num = '\t' * (8 - len(attribute[0]) // 4)
    comment = attribute[1]
    print(f"\t{attribute[0]}{t_num}VARCHAR(255)\t\tNOT NULL\t\tDEFAULT ' '\t\tCOMMENT '{comment}',")

print("""
	MS_RESUME									VARCHAR(300)		NOT NULL		DEFAULT ' '							COMMENT '简述',
	MS_DETAIL									VARCHAR(1000)		NOT NULL		DEFAULT ' '							COMMENT '详细',
	RC_RECORD_TIME								TIMESTAMP			NOT NULL		DEFAULT CURRENT_TIMESTAMP			COMMENT '收录时间',
	RC_RECORDER									VARCHAR(50)			NOT NULL		DEFAULT '未收录'						COMMENT '收录人',
	RC_LAST_MODIFIED_TIME						TIMESTAMP			COMMENT '最后修改时间',
	RC_LAST_MODIFIER							VARCHAR(50)			NOT NULL		DEFAULT '未收录'						COMMENT '最后修改人',
	RC_DATA_STATUS								CHAR(1)				NOT NULL		DEFAULT '0'							COMMENT '数据状态: 0-未生效, 1-正常, 2-不可用,9-废弃',
	CONSTRAINT class_pk PRIMARY KEY (,)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_bin
COMMENT=;
""")