create table user_account (
	id serial primary key,
	username text not null unique,
	password text not null,
	role text not null default 'user',
	emails text[],
	code text
	-- emails text[],
	-- is_deleted boolean default false
);


create table account_creation_code (
	code text,
	description text
);


create table jwt_token (
	token text,
	meta json,
	user_account_id int references user_account(id) on delete cascade
);


create table category(
	id serial primary key,
	title varchar(16),
	caption text,
	is_pinned bool not null default false
);

create table blog_post(
	id serial primary key,
	category_id int references category(id),
	title varchar(64) not null,
	caption text,
	body text not null,
	created_at timestamptz not null default now(),
	updated_at timestamptz
);

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER blog_post_update_trigger
BEFORE UPDATE ON blog_post
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


create table blog_post_comment(
	id serial primary key,
	blog_post_id int references blog_post(id),
	user_name varchar(64),
	body text,
	created_at timestamptz not null default now()
);
