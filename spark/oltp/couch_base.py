from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions, QueryOptions)
username = "Administrator"
password = "password"
bucket_name = "travel-sample"
auth = PasswordAuthenticator(
    username,
    password,
)

cluster = Cluster('couchbase://localhost', ClusterOptions(auth))
cluster.wait_until_ready(timedelta(seconds=5))
# cb = cluster.bucket(bucket_name)
# cb_coll = cb.scope("inventory").collection("airline")
# cb_coll_default = cb.default_collection()

# airline = {
#     "type": "airline",
#     "id": 8091,
#     "callsign": "CBS",
#     "iata": None,
#     "icao": None,
#     "name": "Couchbase Airways",
# }
