PRAGMA foreign_keys=1;



CREATE TABLE leads(	id VARCHAR(10) PRIMARY KEY NOT NULL,
			code VARCHAR(25) UNIQUE ,
			customer_name VARCHAR(100) NOT NULL,
			address_line1 VARCHAR(50),
			address_line2 VARCHAR(50),
			address_line3 VARCHAR(50),
			area_name VARCHAR(50),
			pincode	  VARCHAR(6),
			city VARCHAR(50),
			state VARCHAR(50));
