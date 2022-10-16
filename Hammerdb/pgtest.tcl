puts "setting config"
dbset db pg
diset connection pg_host localhost
diset connection pg_port 5432
diset tpcc pg_superuser aayush
diset tpcc pg_superuserpass pass11
diset tpcc pg_storedprocs false
diset tpcc pg_vacuum true
diset tpcc pg_driver timed
diset tpcc pg_rampup 2
diset tpcc pg_duration 2
vuset logtotemp 1
vuset unique 1
tcset logtotemp 1
tcset timestamps 1
loadscript
puts "TEST STARTED"
vuset vu 5
vucreate
tcstart
tcstatus
vurun
puts "RUNTIMER STARTED"
runtimer 300
print dict
vudestroy
tcstop
puts "TEST COMPLETE"
