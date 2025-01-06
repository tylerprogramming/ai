table_schema: public
table_name: leads
columns:
  id:
    data_type: integer
    is_nullable: NO
    column_default: nextval('leads_id_seq'::regclass)
  first_name:
    data_type: character varying
    is_nullable: NO
    column_default: null
  last_name:
    data_type: character varying
    is_nullable: NO
    column_default: null
  email:
    data_type: character varying
    is_nullable: NO
    column_default: null
  phone_number:
    data_type: character varying
    is_nullable: YES
    column_default: null
  company:
    data_type: character varying
    is_nullable: YES
    column_default: null
  job_title:
    data_type: character varying
    is_nullable: YES
    column_default: null
  lead_source:
    data_type: character varying
    is_nullable: YES
    column_default: null
  created_at:
    data_type: timestamp without time zone
    is_nullable: YES
    column_default: now()