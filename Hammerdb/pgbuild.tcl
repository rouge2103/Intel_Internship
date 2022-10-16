dbset db pg
diset connection pg_host localhost
diset connection pg_port 5432
diset tpcc pg_count_ware 5
diset tpcc pg_num_vu 5
diset tpcc pg_superuser aayush
diset tpcc pg_superuserpass pass11
diset tpcc pg_storedprocs false
vuset logtotemp 1
vuset unique 1
buildschema
