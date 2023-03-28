CREATE table capstone2.status (

facility_uid VARCHAR(255),
operation_status VARCHAR(255),
registration_status VARCHAR(255),
license_status VARCHAR(255)

);


CREATE table capstone2.services (
facility_uid VARCHAR(255),
outpatient_service VARCHAR(255),
ambulance_services VARCHAR(255),
mortuary_services VARCHAR(255),
onsite_imaging VARCHAR(255),
onsite_pharmarcy VARCHAR(255),
onsite_laboratory VARCHAR(255),
tot_num_beds int,
special_service VARCHAR(255),
dental_service VARCHAR(255),
pediatrics_service VARCHAR(255),
gynecology_service VARCHAR(255),
surgical_service VARCHAR(255),
medical_service VARCHAR(255),
inpatient_service VARCHAR(255)

);
CREATE table capstone2.personnel (

facility_uid VARCHAR(255),
num_of_docs int,
num_of_pharms int,
num_of_midwifes int,
num_of_nurses int,
num_of_nurse_midwife int,
num_of_pharm_technicians int,
num_of_dentists int,
num_of_health_attendants int,
num_of_env_health_officers int,
num_of_him_officers int,
num_of_community_health_officer int,
num_of_jun_community_extension_worker int,
num_of_community_extension_workers int,
num_of_dental_technicians int,
num_of_lab_technicians int,
num_of_lab_scientists int

);

CREATE table capstone2.pages (

facility_uid VARCHAR(255) PRIMARY KEY,
state VARCHAR(255),
lga VARCHAR(255),
ward VARCHAR(255),
facility_code VARCHAR(255),
facility_name VARCHAR(255),
facility_level VARCHAR(255),
ownership  VARCHAR(255)

);

CREATE table capstone2.locations (

facility_uid VARCHAR(255),
state VARCHAR(255),
lga VARCHAR(255),
ward VARCHAR(255),
physical_location VARCHAR(255),
postal_address VARCHAR(255),
longitude NUMERIC(5,2),
latitude  NUMERIC(5,2)

);
CREATE table capstone2.contacts (

facility_uid VARCHAR(255),
phone_number VARCHAR(255),
alternate_number VARCHAR(255),
email_address VARCHAR(255),
website VARCHAR(255)
);
CREATE table capstone2.identifiers (

facility_uid VARCHAR(255),
facility_code VARCHAR(255),
state_unique_id VARCHAR(255),
registration_no VARCHAR(255),
facility_name VARCHAR(255),
alternate_name VARCHAR(255),
start_date Date,
ownership VARCHAR(255),
ownership_type VARCHAR(255),
facility_level VARCHAR(255),
facility_level_option VARCHAR(255),
days_of_operation VARCHAR(255),
hours_of_operation VARCHAR(255)
);

select * from capstone2.pages ;
select * from capstone2.status;
select * from capstone2.personnel;
select * from capstone2.services;
select * from capstone2.locations;
select * from capstone2.contacts;
select * from capstone2.identifiers;
