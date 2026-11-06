#!/usr/bin/env python

import os
import xml.etree.ElementTree as ETree
from time import strftime
import ipaddress

import requests

# Domains to update.
domains = (
    "PUT_URL_HERE",
)
record_ttl = "3600"

#######################################################################################################################
#######################################################################################################################
#  STOP EDITING!                 You're done!  Congratulations.  Now give us a whirl!                   STOP EDITING! #
#######################################################################################################################
#######################################################################################################################
namesilo_api_key = os.environ.get('NAMESILO_API_KEY')
NAMESILO_COM_API = 'https://www.namesilo.com/apibatch'
NAMESILO_API_IMPLEMENTED_OPERATIONS = {'dnsListRecords', 'dnsUpdateRecord'}

_web_worker = requests.session()  # Requests session instance.


class NameSilo_APIv1:
    def __init__(self, domain):
        print(f'NameSilo connection called for {domain} at {strftime('%x %H:%M:%S')}.')
        self.domain = domain
        self._namesilo_api_params = {
            'version': '1',
            'type': 'xml',
            'key': namesilo_api_key,
            'domain': self.domain
        }
        self.current_records = []  # NameSilo's current resource records for self.domain retrieved from the API.

        self.retrieve_resource_records()  # populate.

    @property
    def domain(self) -> str:
        """The domain to be manipulated."""
        return self._domain

    @domain.setter
    def domain(self, value):
        if value is not None:
            self._domain = value
        else:
            raise ValueError('Invalid domain name. Please specify a domain in normal syntax, e.g.: google.com')

    def _api_connection(self, operation, **html_params) -> ETree.ElementTree:
        """Connection endpoint. Returns operations in XML as Element"""
        if operation is not None and operation in NAMESILO_API_IMPLEMENTED_OPERATIONS:
            _api_call = {**html_params, **self._namesilo_api_params}  # Join request parameter dicts.
            _api_url = str.join('/', [NAMESILO_COM_API, operation])  # Build URL with operation.
            # print('API connection:', _api_url, _api_call)
            _ret = _web_worker.get(_api_url, params=_api_call)  # Send the API request.
            _ret.raise_for_status()  # Builtin check for HTTP success.
            _ret = ETree.XML(_ret.text)  # The final form of our return response.
            """Response Validation"""
            try:
                success = _ret.find('.//reply/code').text
            except AttributeError:
                raise ValueError('Could not parse API response.')
            if success != '300':
                raise ValueError(f'API Operation failed with code {success}.')
            return _ret
        else:
            raise NotImplementedError(f'Invalid operation: {operation} is currently unsupported or undefined.')

    def retrieve_resource_records(self):
        """Retrieve current Resource Records from NameSilo for self.domain."""
        print(f'Retrieving records for {self.domain}')
        current_records = self._api_connection('dnsListRecords')
        self.current_records = []
        for current_resource_record in current_records.iter('resource_record'):
            self.current_records.append(
                dict(
                    (resource_record.tag, resource_record.text)
                    for resource_record
                    in current_resource_record.iter()
                )
            )
        print(f'{len(self.current_records)} records retrieved for {self.domain}')
        for record in self.current_records:
            print(record)
        print()

    def dynamic_dns_update(self, value, type=None):
        """Dynamic DNS updater"""
        # If no type given, assume an IP value in, otherwise, type must be given
        # Because we don't know what kind of type user want
        if not type:
            try:
                ip_address = ipaddress.ip_address(value)
            except ValueError:
                print(f'{value} is not a valid IPv4/IPv6 address, type must be given')
                return
            if(ip_address.version == 4):
                type = 'A'
            else:
                type = 'AAAA'
        print(f'DDNS update starting for domain: {self.domain} and record type {type}')
        # Generator for hosts that require an record update.
        hosts_requiring_updates = (
            record for record
            in self.current_records
            if record['type'] == type
            and record['value'] != value
        )

        # Now iterate and send requests to the endpoint to update those hosts.
        _count = 0
        _failed = 0
        for host in hosts_requiring_updates:
            print(f'DDNS update required for {host}')
            __api_params = {
                'rrid': host['record_id'],
                'rrhost': host['host'],
                'rrvalue': value,
                'rrttl': record_ttl,
            }
            try:
                self._api_connection('dnsUpdateRecord', **__api_params)
            except ValueError:
                print(f'DDNS failed to update {host['host']}')
                _failed += 1
                pass
            except NotImplementedError:
                print(f'DDNS failed to update {host['host']}')
                _failed += 1
                pass
            _count += 1
            print(f'DDNS successfully updated {host['host']}')
        print(f'DDNS update complete for {self.domain}. {_count} hosts required updates. {_failed} errors.')


def update_records(current_ip):
    print(f"DDNS operation started at {strftime('%x %H:%M:%S')}")
    print(f"current IP address is {current_ip}")
    for domain in domains:
        NameSilo_APIv1(domain).dynamic_dns_update(current_ip)


if __name__=="__main__":
    current_ip = _web_worker.get('https://api.ipify.org/?format=json').json()['ip']  # GET our current IP.
    update_records(current_ip)
