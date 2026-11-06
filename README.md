# NameSilo API Python3 Implementation - Specifically for DDNS support.

NameSilo Dynamic DNS IP Address Updater.
Forked from https://github.com/rbenji/DynamicDNS-for-NameSilo

# REQUIRES
 - Python >= 3.6,
 - Requests (http://docs.python-requests.org/)
  `pip install requests`

## Configuration
- Example configuration for a single domain with hosts:
```
 record_ttl = '7207'
 domains = (
     "namesilo.com",
 )
```

# Usage Examples

## Update/Add IPv4/IPv6 record

The following 2 lines will update all records of xxx.com to 1.2.3.4

```python
import ddns_manager
api = ddns_manager.NameSilo_APIv1("xxx.com")
api.dynamic_dns_update("1.2.3.4")
```

# How To

1. Generate and save an API key from NameSilo. See [NameSilo](https://www.namesilo.com/Support/Account-Options) for help.
2. Create copies of the script as needed and configure them.
3. Export required ENVIRONMENT VARIABLES: NAMESILO_API_KEY
4. Save the python file and run it using `python <whateverYouNamedIt>.py`.  Some systems may run two versions of python: `python3 <whateverYouNamedIt>.py`
5. (optional) Add this command to cron or scheduler depending, ya know?

You can also use this as a class in your own programs, though it is a rather immature implementation as of writing.
