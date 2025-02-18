# Networking in Google Cloud

## Virtual Private Clouds
Virtual Private Clouds (VPC) are software abstractions that act like a physical network. They are used to link resources in a project together, and Google autoamtically creates one when you create a new project.

VPCs are global resources, not tied to regions or zones. They can contain subnets, which are regional resources that are associated with a range of IP addresses. Subnets provide private internal addresses that resources can use to communicate with each other and with Google APIs.

You can also create a shared VPC within an organization. This shared VPC is hosted in a common project, and users from other projects can create and use VPC resources as long as they have adequate permissions. Network Peering is another means of communication supported by Google Cloud.

### Create a VPC

*Using Cloud Console*
1. Navigate to VPC Networks page.
2. Click `Create VPC Network`.
3. Assign a name and description.
4. Choose Custom or Automatic for Subnet creation.
    - Automatic: subnets are created in each region automatically, Google chooses the range of IP addresses.
    - Custom: Create your own subnets, specify region and IP address range in CDIR notation.
    - Toggle Private Google Access to allow VMs on the subnet to access GCP services without assigning an external IP address to the VM.
    - Toggle logging of network traffic using `Flow Logs` option.
5. Choose Firewall Rules.
6. Choose Regional or Global Dynamic Routing.
7. Optionally choose DNS Server Policy.

*Using Cloud SDK*
1. Create a VPC in the default project with automatic subnets:

        gcloud compute networks create ace-exam-vpc1 --subnet-mode=auto

2. Create a VPC with custom subnets:

        gcloud compute networks create ace-exam1-vpc1 --subnet-mode=custom
        
        gcloud compute networks subnets create ace-exam-vpc-subnet1 \
            --network=ace-exam-vpc1 --region=us-central1 --range=10.10.0.0/16 \
            --enable-private-ip-google-access --enable-flow-logs

3. Create a Shared VPC :
    - First, you need to assign an organization member the Shared VPC Admin role at the organization/folder level.
    
            gcloud organizations add-iam-policy-binding [ORG_ID] \
                --member='user:[email_address]'
                --role="roles/compute.xpnAdmin"
    
        OR
            
            gcloud resource-manager folders add-iam-policy-binding [FOLDER_ID] \
                --member='user:[email_address]'
                --role="roles/compute.xpnAdmin"
            
    - You can find the organization ID using `gcloud organizations list` and the folder ID using `gcloud resource-manager folders list --organization=[ORG_ID]`.
    
    - Issue the `shared-vpc` command:
    
            gcloud compute shared-vpc enable [HOST_PROJECT_ID]
            
    - Associate projects to the VPC:
    
            gcloud compute shared-vpc associated-projects add [SERVICE_PROJECT_ID] \
                --host-project [HOST_PROJECT_ID]
                
    - If an organization doesn't exist, you can alternatively use VPC network peering:
    
            gcloud compute networks peerings create peer-ace-exam-1 \
                --network ace-exam-network-A \
                --peer-project ace-exam-project-B \
                --peer-network ace-exam-network-B \
                --auto-create-routes
    
            gcloud compute networks peerings create peer-ace-exam-1 \
                --network ace-exam-network-B \
                --peer-project ace-project-A \
                --peer-network ace-exam-network-A \
                --auto-create-routes
    
    - This will allow private traffic to flow between VPCs.

### CIDR Notation
Classless Interdomain Routing (CIDR) is a notation for specifying a range of IP addresses. It consists of a network address for identifying a subnet and a network mask. Example:
- 10.0.0.0 - 10.255.255.255 (/8)
- 172.16.0.0 - 172.31.255.255 (/12)
- 192.168.0.0 - 192.168.255.255 (/16)

The network mask is a number of bits from the start of the IP address that denote the network host. Every bit that is not masked represents the total node capacity of the network.

The CIDR expression `0.0.0.0/0` denotes a network with hosts with IP addresses 0.0.0.0 - 255.255.255.255, whereas the expression `0.0.0.0/16` denotes a network with hosts with IP addresses 0.0.0.0 - 0.0.255.255.

### Deploy Compute Engine with a Custom Network

*Using Cloud Console*
1. Navigate to Compute Engine and click `Create Instance`.
2. In the menu towards the bottom, click `Management` -> `Security` -> `Disks` -> `Networking` -> `Sole Tenancy` to expand optional forms and select the `Networking` tab.
3. Click `Add Network Interface` to display a page where you can choose a custom network.
4. Specify a static IP address or choose a custom ephemeral address.

*Using Cloud SDK*
1. Use normal `compute instance create` command, but include the parameters `subnet` and `zone`:

        gcloud compute instances create [INSTANCE_NAME] --subnet [SUBNET_NAME] --zone [ZONE_NAME]


### Create Firewall Rules for VPC
Firewall rules are defined at the network level and are used to allow or restrict specific types of traffic on a port. For example: a rule may allow TCP traffic to port 22.

Traffic can be `ingress` (incoming) or `egress` (outgoing).

All firewall rules have:
- Direction (ingress or egress)
- Priority (0 to 65535, default is 65534)
- Action (allow or deny)
- Target (instance(s) to which the rule applies)
- Source/Destination (IP ranges, network tags, or instances using a specific service account)
- Protocol (TCP, HTTP, UDP, ICMP, etc., default is all protocols)
- Port
- Enforcement Status (enabled or disabled)

VPCs have some default rules with priority 65534:
- Allow incoming traffic from any VM instance on the same network.
- Allow incoming traffic on port 22, allowing SSH.
- Allow incoming TCP traffic on port 3389, allowing Remote Desktop Protocol (RDP).
- Incoming Internet Control Message Protocol (ICMP) from any source on the network.

There are also 2 implied rules with priority 65535 (so they are easily overriden):
- Allow all egress traffic to all destinations.
- Deny all ingress traffic from all sources.

*Using Cloud Console*
1. Navigate to VPCs in the Console and select `Firewall` from the menu.
2. Click `Create Firewall Rule`.
3. Specify the name, description, and the network in the VPC to apply the rule to.
4. (Optionally) enable logging.
5. Specify all the attributes listed above (direction, priority, action, target, source/destination, protocol, port, enforcement)

*Using Cloud SDK*
Example:

    gcloud compute firewall-rules create ace-exam-fwr2 --network ace-exam-vpc1 --allow tcp:20000-25000
    
Can also use these parameters: action, allow, description, destination-ranges, direction, network, priority, source-ranges, source-service-accounts, source-tags, target-service-accounts, target-tags

## Virtual Private Networks
A Virtual Private Network (VPN) allows you to securely send network traffic from the Google network to your own network.

### Create a VPN
*Using Cloud Console*
1. Navigate to the `Hybrid Connectivity` section of the console.
2. Click `Create VPN Connection`.
3. Choose either a High-Availability VPN or a classic VPN.
    - HA supports dynamic routing using Border Gate Protocol and a high availability 99.99 SLA.
    - Classic allows dynamic routing, but not for connections outside of Google Cloud, so if connecting from outside GCP, use HA.
4. Specify gateway name, network, and region.
5. Add VPN tunnels to connect the VPN gateway to a peer gateway.
6. Specify the other network endpoint (name, description, IP address).

*Using Cloud SDK*
1. Create a Classic VPN:

        gcloud compute vpn-tunnels create NAME --peer-address=PEER_ADDRESS \
            --shared-secret=SHARED_SECRET --target-vpn-gateway=TARGET_VPN_GATEWAY
            
2. Creating a HA VPN requires the parameter `--peer-gcp-gateway` or `--peer-external-gateway`.
3. Create forwarding rules:

        gcloud compute forwarding-rules create NAME --TARGET_SPECIFICATION=VPN_GATEWAY
        
4. Create VPN tunnels:

        gcloud compute vpn-tunnels create NAME --peer-address=PEER_ADDRESS \
            --shared_secret=SHARED_SECRET --target-vpn-gateway=TARGET_VPN_GATEWAY

## Cloud DNS
DNS stands for "Domain Name System" and is a way to map domain names to IP addresses. Google has a maanged service called "Cloud DNS" for providing this service with high availability, low latency, and scalability.

Using Cloud DNS, you can create a managed zone which contains records associated with a DNS name suffix and also contains details about the zone.

*Create a Zone with Cloud Console*
1. Navigate to `Network Services` in Cloud Console and select `Cloud DNS`.
2. Click `Create Zone` and specify some information:
    - Zone type (Public/Private)
        - Public zones are accessible via the public Internet.
        - Private zones provide name services to GCP resoruces like VMs or load balancers and are only accessible from within the project.
    - Zone name (unique within project)
    - DNS name (myzone.example.com)
    - Description
    - DNSSEC
        - Security measure that provides strong authentication and protects against spoofing and cache poisoning.
    - If making a Private zone, choose the networks that will have access.
    - Enable Cloud Logging
    
*Create a Zone with Cloud SDK*
1. Create a Public DNS Zone:

        gcloud dns managed-zones create ace-exam-zone1 --description="A sample zone" --dns-name=aceexamzone.com.
    
2. Create a Private Zone:

        gcloud dns managed-zones create ace-exam-zone1 --description="A sample private zone" \
                --dns-name=aceexamzone.com. --visibility=private --networks=default
        
3. Add an `A` and a `CNAME` record:

        gcloud dns record-sets transaction start --zone=ace-exam-zone1
        gcloud dns record-sets transaction add 192.0.2.91 --name=aceexamezone.com. \
                --ttl=300 --type=A --zone=ace-exam-zone1
        gcloud dns record-sets transaction add server1.aceexamzone.com. \
        --name=www2.aceexamzone1.com. --ttl=300 --type=CNAME --zone=ace-exam-zone1
        gcloud dns record-sets transaction execute --zone=ace-exam-zone1
        
When you create a zone, some records are added automatically:
- `NS` is a name server records that has the address of an authoritative server that manages the zone info.
- `SOA` is a start-of-authority record which has authoritative info about the zone.

You can add other records such as `CNAME` (Canonical name), `A`, and `AAAA` records. When creating a record, you can specify TTL (time to live) parameters to denote how long the record can live in cache before DNS resolvers query for the value again. DNS does this by performing lookup operations that map domains to IP addresses, and you can configure it to map a domain to multiple IP addresses.
    
## Load Balancing
Load Balancers distribute workload to servers running an application. They can distribute load within a single region or multiple regions. Google Cloud offers different load balancers that are characterized by key features:
- Global vs regional load balancing.
- External vs internal load balancing.
- Type of traffic (HTTP, TCP, etc.)

For Global balancers, there are 4 options:
1. Global External HTTP(S) for balancing HTTP and HTTPS loads across back-end instances globally on a Premium network service tier.
2. Global External HTTP(S) (classic) for balancing HTTP and HTTPS loads across back-end instances globally on Premium tier networking and regionally on Standard tier networking.
3. SSL Proxy which terminates SSL/TLS connections, used for non-HTTPS traffic.
4. TCP Proxy which terminates TCP sessions at the load balancer and then forwards traffic to back-end servers.

Regional load balancers are for when an application only needs to be distribute in a single region. There are 4 options:
1. Regional External HTTP(S) for balancing HTTP and HTTPS regionally on Standard tier networking.
2. Internal HTTP(S) for balancing HTTP and HTTPS regionally on Premium tier networking.
3. Internal TCP/UDP for balacning TCP/UDP regionally on Premium tier networking.
4. External TCP/UDP for balancing TCP, UDP, and other protocols regionally on Standard or Premium tier networking.

Load balancing is incredibly important for services that need to be highly available because it allows you to distribute traffic and monitor the health of VMs. For example, if you are providing API access to customer data, you must consider how to scale up and down in response to changes in load and how to ensure HA.
- Combining Instance Groups and Load Balancing solves both problems. Instance Groups manage auto-scaling while load balancing monitors the health of VMs.

*Configuring Load Balancers in Cloud Console*
1. Navigate to `Network Services` and select `Load Balancing`.
2. Choose which type of load balancer to create; for example, a TCP load balancer.
3. Select "Only Between My VMs" for private load balancing.
4. Select single-region or multi-region.
5. Specify backend type.
    - Backend Service allows has support for connection draining, TCP health checks, managed instance groups, and failover groups.
    - Target Pools are instances in a region that are identified by a list of URLs that specify what VMs can receive traffic.
6. Configure Health Check for the back end.
    - Specify name, protocol, port, and health criteria.
7. Configure the front end.
    - Specify name, subnetwork, internal IP configuration, and the port that will have its traffic forwarded to the backend (for example, port 80).
    
*Configuring Load Balancers with Cloud SDK*
1. Use this command to create a Target Pool:

        gcloud compute target-pools create ace-exam-pool --description="example target pool" \
                --region=us-central1
                
2. Use this command to add instances to the Target Pool:

        gcloud compute target-pools add-instances ace-exam-pool --instances ex1 ex2

3. Use this command to forward traffic from any VM in the ace-exam-pool to the load balancer:

        gcloud compute forwarding-rules create ace-exam-lb --port=80 --target-pool ace-exam-pool

## Google Private Access

## IP Addressing