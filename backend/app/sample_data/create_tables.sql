-- drop schema sample_data cascade

-- truncate sample_data.customer
-- truncate sample_data.lineitem
-- truncate sample_data.nation
-- truncate sample_data.orders
-- truncate sample_data.part
-- truncate sample_data.partsupp
-- truncate sample_data.region
-- truncate sample_data.supplier

create table if not exists sample_data.customer
(
	c_custkey DECIMAL not null,
	c_name VARCHAR(25) not null,
	c_address VARCHAR(40) not null,
	c_nationkey DECIMAL not null,
	c_phone VARCHAR(15) not null,
	c_acctbal DECIMAL(12,2) not null,
	c_mktsegment VARCHAR(10),
	c_comment VARCHAR(117)
);

create table if not exists sample_data.lineitem
(
	l_orderkey DECIMAL not null,
	l_partkey DECIMAL not null,
	l_suppkey DECIMAL not null,
	l_linenumber DECIMAL not null,
	l_quantity DECIMAL(12,2) not null,
	l_extendedprice DECIMAL(12,2) not null,
	l_discount DECIMAL(12,2) not null,
	l_tax DECIMAL(12,2) not null,
	l_returnflag VARCHAR(1) not null,
	l_linestatus VARCHAR(1) not null,
	l_shipdate DATE not null,
	l_commitdate DATE not null,
	l_receiptdate DATE not null,
	l_shipinstruct VARCHAR(25) not null,
	l_shipmode VARCHAR(10) not null,
	l_comment VARCHAR(44) not null
);

create table if not exists sample_data.nation
(
	n_nationkey DECIMAL not null,
	n_name VARCHAR(25) not null,
	n_regionkey DECIMAL not null,
	n_comment VARCHAR(152)
);

create table if not exists sample_data.orders
(
	o_orderkey DECIMAL not null,
	o_custkey DECIMAL not null,
	o_orderstatus VARCHAR(1) not null,
	o_totalprice DECIMAL(12,2) not null,
	o_orderdate DATE not null,
	o_orderpriority VARCHAR(15) not null,
	o_clerk VARCHAR(15) not null,
	o_shippriority DECIMAL not null,
	o_comment VARCHAR(79) not null
);

create table if not exists sample_data.part
(
	p_partkey DECIMAL not null,
	p_name VARCHAR(55) not null,
	p_mfgr VARCHAR(25) not null,
	p_brand VARCHAR(10) not null,
	p_type VARCHAR(25) not null,
	p_size DECIMAL not null,
	p_container VARCHAR(10) not null,
	p_retailprice DECIMAL(12,2) not null,
	p_comment VARCHAR(23)
);

create table if not exists sample_data.partsupp
(
	ps_partkey DECIMAL not null,
	ps_suppkey DECIMAL not null,
	ps_availqty DECIMAL not null,
	ps_supplycost DECIMAL(12,2) not null,
	ps_comment VARCHAR(199)
);

create table if not exists sample_data.region
(
	r_regionkey DECIMAL not null,
	r_name VARCHAR(25) not null,
	r_comment VARCHAR(152)
)
;

create table if not exists sample_data.supplier
(
	s_suppkey DECIMAL not null,
	s_name VARCHAR(25) not null,
	s_address VARCHAR(40) not null,
	s_nationkey DECIMAL not null,
	s_phone VARCHAR(15) not null,
	s_acctbal DECIMAL(12,2) not null,
	s_comment VARCHAR(101)
);