DROP table tmp_kgs_commodity_token_100000;

CREATE TABLE if not exists tmp_kgs_commodity_token_100000
(
uid       STRING COMMENT '手机号',
token_t   MAP<STRING,STRING> COMMENT 'token'
) 
comment "签名发送短信统计表"
-- PARTITIONED BY (ds STRING) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
COLLECTION ITEMS TERMINATED BY '\073'
MAP KEYS TERMINATED BY '\072'
STORED AS TEXTFILE;

-- 随机抽样
INSERT INTO tmp_kgs_commodity_token_100000
SELECT
uid,
token_t
FROM adl_limao_commodity_token_agg
order by rand() 
limit 100000;

-- 结果随机排列
SELECT *
FROM tmp_kgs_commodity_token_100000
order by rand() 

load data local inpath '/data1/shell/data_tool/tmp/config_token_keywords_reduction.csv' 
overwrite into table config_token_keywords_reduction;

Drop table config_token_keywords_reduction;
CREATE TABLE config_token_keywords_reduction
(
keyword   STRING,
category  STRING,
weight    FLOAT
)
-- comment "物品描述关键词降维矩阵"
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE;

SELECT *
FROM config_token_keywords_reduction
limit 100;
