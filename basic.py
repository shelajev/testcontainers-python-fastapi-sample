from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for, wait_container_is_ready
import requests
import time


opensearch = DockerContainer("opensearchproject/opensearch:2.2.0")
opensearch.with_env("discovery.type", "single-node")
opensearch.with_exposed_ports(9200)

def get_url(opensearch):
    return f"http://{opensearch.get_container_host_ip()}:{opensearch.get_exposed_port(9200)}"

@wait_container_is_ready(requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout)
def _connect(opensearch):
    url = get_url(opensearch)
    response = requests.get("{}/_plugins/_security/health".format(url), timeout=1)
    response.raise_for_status()

with opensearch:
    print("our url =", get_url(opensearch))
    time.sleep(5)
    print('done')

















#
# opensearch = DockerContainer('opensearchproject/opensearch:2.2.0')
# opensearch.with_env("discovery.type", "single-node")
# opensearch.with_exposed_ports(9200)
#

