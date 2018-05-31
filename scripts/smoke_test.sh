#!/bin/bash
export DATA_DIR=/c/repo/rest-service-example/app/tests/integration/
curl -i -H "Accept: application/json" "http://localhost:8086/customers/2e38c4da-600f-11e8-b3e7-0242ac1a0003"
curl "http://localhost:8086/customers/" -d @${DATA_DIR}test_customer01.json --header "Content-Type: application/json"
