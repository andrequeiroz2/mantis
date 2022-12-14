CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE public.users (
	id int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY,
	username varchar(50) NOT NULL,
	email varchar(60) NOT NULL,
	useruid uuid DEFAULT uuid_generate_v4(),
	"password" varchar(120) NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (id)
);
CREATE UNIQUE INDEX users_email_idx ON public.users USING btree (email);
CREATE UNIQUE INDEX users_username_idx ON public.users USING btree (username);
