# NameSilo API Python3 Implementation - Specifically for DDNS support.

NameSilo Dynamic DNS IP Address Updater.
Forked from https://github.com/rbenji/DynamicDNS-for-NameSilo

# REQUIRES
 - Python >= 3.6,
 - Requests (http://docs.python-requests.org/)
  `pip install requests`

## Configuration
- Example configuration for a single domain with hosts (without email notification):
```
 record_ttl = '7207'
 domains_and_hosts = (
     ["namesilo.com", ["", "www", "mail"]],  # This will update namesilo.com, www.namesilo.com, and mail.namesilo.com.
 )
```
- Example configuration for multiple domains and hosts (without email notification):
```
 record_ttl = '7207'
 domains_and_hosts = (
     ["namesilo.com", ["www", "mail"]],  # This will update www.namesilo.com, and mail.namesilo.com.
     ["CNN.com", ["", "www"]],  # This will update CNN.com, and www.CNN.com.
     ["NPR.org", ["giving", "charity"]],  #  This will update giving.NPR.org, and charity.NPR.org.
     ["example.org", [""]]  #  This will update example.org.
 )
```

# Usage Examples

## Update/Add IPv4/IPv6 record

The following 2 lines will update A record of www.xxx.com and test.xxx.com to 1.2.3.4, if any of them doesn't exist, it will be created automatically

```python
import ddns_manager
api = ddns_manager.NameSilo_APIv1("xxx.com", ["www", "test"])
api.dynamic_dns_update("1.2.3.4")
```

## Update/Add specific type record

The valid type will be:

- A - The IPV4 Address
- AAAA - The IPV6 Address
- CNAME - The Target Hostname
- MX - The Target Hostname
- TXT - The Text

The following 2 lines will update/create a TXT record of _acme-challenge.xxx.com and its value is utpEMa5B58CMdjTJCLnB5XxcmZ0CoCP6PFdmqE5bIpo.

```python
import ddns_manager
api = ddns_manager.NameSilo_APIv1("xxx.com", ["_acme-challenge"])
api.dynamic_dns_update("utpEMa5B58CMdjTJCLnB5XxcmZ0CoCP6PFdmqE5bIpo", "TXT")

# You may want to create a record without checking if it exists or not.
api.dynamic_dns_add("www", "2001::3", "AAAA")
```

## Delete record

This delete function will delete all the records which match the conditions user offered. User can offer host, value, type as delete function paramter, all the parameters are optional.
If no parameter given, means all the namesilo records belongs to this domain will be deleted.

```python
import ddns_manager

api = ddns_manager.NameSilo_APIv1("xxx.com")

# Delete _acme-challenge.xxx.com TXT record with value utpEMa5B58CMdjTJCLnB5XxcmZ0CoCP6PFdmqE5bIpo
api.dynamic_dns_delete("_acme-challenge", "utpEMa5B58CMdjTJCLnB5XxcmZ0CoCP6PFdmqE5bIpo", 'TXT')

# Delete all AAAA records
api.dynamic_dns_delete(type="AAAA")

# Delete all www records
api.dynamic_dns_delete(host_without_domain="www")

# Delete all records which value is "4.5.6.7"
api.dynamic_dns_delete(value="4.5.6.7")

# Delete any records belongs to this domain
api.dynamic_dns_delete()
```


# How To

1. Generate and save an API key from NameSilo. See [NameSilo](https://www.namesilo.com/Support/Account-Options) for help.
2. Create copies of the script as needed and configure them.
3. Export required ENVIRONMENT VARIABLES: NAMESILO_API_KEY
4. Save the python file and run it using `python <whateverYouNamedIt>.py`.  Some systems may run two versions of python: `python3 <whateverYouNamedIt>.py`
5. (optional) Add this command to cron or scheduler depending, ya know?

You can also use this as a class in your own programs, though it is a rather immature implementation as of writing.
