# Lookups

* AS
* Ip (multiple)
* Basic DNS

# Object Model

## Url

* Track entire URL
* Time the URL was queried
* Tracks overall query process
* Has one or more DNS Entries
* Points to an FQDN for base hostname
* Points to DnsEntries

## FQDN

* Basic hostname
* One or more IPs

## DnsEntry

* Tracks the type and result of a Dns Entry

## AS

* Range
* Location


# Architecture

* Have a single node endpoint that distributes the query out to other node 
  endpoints, so that the django query will always go through