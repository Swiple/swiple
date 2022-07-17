create database sample_data

create or replace table tpch_sf1.customer
(
	c_custkey NUMBER not null,
	c_name VARCHAR(25) not null,
	c_address VARCHAR(40) not null,
	c_nationkey NUMBER not null,
	c_phone VARCHAR(15) not null,
	c_acctbal NUMBER(12,2) not null,
	c_mktsegment VARCHAR(10),
	c_comment VARCHAR(117)
)
comment = 'Customer data as defined by TPC-H';

create or replace table tpch_sf1.lineitem
(
	l_orderkey NUMBER not null,
	l_partkey NUMBER not null,
	l_suppkey NUMBER not null,
	l_linenumber NUMBER not null,
	l_quantity NUMBER(12,2) not null,
	l_extendedprice NUMBER(12,2) not null,
	l_discount NUMBER(12,2) not null,
	l_tax NUMBER(12,2) not null,
	l_returnflag VARCHAR(1) not null,
	l_linestatus VARCHAR(1) not null,
	l_shipdate DATE not null,
	l_commitdate DATE not null,
	l_receiptdate DATE not null,
	l_shipinstruct VARCHAR(25) not null,
	l_shipmode VARCHAR(10) not null,
	l_comment VARCHAR(44) not null
)
comment = 'Lineitem data as defined by TPC-H';

create or replace table tpch_sf1.nation
(
	n_nationkey NUMBER not null,
	n_name VARCHAR(25) not null,
	n_regionkey NUMBER not null,
	n_comment VARCHAR(152)
)
comment = 'Nation data as defined by TPC-H';

create or replace table tpch_sf1.orders
(
	o_orderkey NUMBER not null,
	o_custkey NUMBER not null,
	o_orderstatus VARCHAR(1) not null,
	o_totalprice NUMBER(12,2) not null,
	o_orderdate DATE not null,
	o_orderpriority VARCHAR(15) not null,
	o_clerk VARCHAR(15) not null,
	o_shippriority NUMBER not null,
	o_comment VARCHAR(79) not null
)
comment = 'Orders data as defined by TPC-H';

create or replace table tpch_sf1.part
(
	p_partkey NUMBER not null,
	p_name VARCHAR(55) not null,
	p_mfgr VARCHAR(25) not null,
	p_brand VARCHAR(10) not null,
	p_type VARCHAR(25) not null,
	p_size NUMBER not null,
	p_container VARCHAR(10) not null,
	p_retailprice NUMBER(12,2) not null,
	p_comment VARCHAR(23)
)
comment = 'Part data as defined by TPC-H';

create or replace table tpch_sf1.partsupp
(
	ps_partkey NUMBER not null,
	ps_suppkey NUMBER not null,
	ps_availqty NUMBER not null,
	ps_supplycost NUMBER(12,2) not null,
	ps_comment VARCHAR(199)
)
comment = 'Partsupp data as defined by TPC-H';

create or replace table tpch_sf1.region
(
	r_regionkey NUMBER not null,
	r_name VARCHAR(25) not null,
	r_comment VARCHAR(152)
)
comment = 'Region data as defined by TPC-H';

create or replace table tpch_sf1.supplier
(
	s_suppkey NUMBER not null,
	s_name VARCHAR(25) not null,
	s_address VARCHAR(40) not null,
	s_nationkey NUMBER not null,
	s_phone VARCHAR(15) not null,
	s_acctbal NUMBER(12,2) not null,
	s_comment VARCHAR(101)
)
comment = 'Supplier data as defined by TPC-H';
