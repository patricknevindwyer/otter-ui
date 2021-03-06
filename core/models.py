from django.db import models
import uuid
import json

# Create your models here.

class Url(models.Model):
    """
    Our root model - the URL is what we branch everything else off of.
    """
    url = models.CharField(max_length=65535, null=False, blank=False)
    fqdn = models.CharField(max_length=65535, null=False, blank=False)
    queriedAt = models.DateTimeField(auto_now=True, null=False, blank=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=False, blank=False)
    dns = models.TextField(null=True, blank=True)

    def json(self):
        return {
            "url": self.url,
            "fqdn": self.fqdn,
            "queriedAt": str(self.queriedAt),
            "uuid": str(self.uuid)
        }

    def formattedDns(self):
        if self.dns is not None:
            return json.dumps(json.loads(self.dns), indent=4)
        else:
            return ""

    def hasMX(self):
        """
        Determine if this Url has a useful set of MX records.

        :return: True or False
        """
        allmxs = []
        [[allmxs.append(mxRecord["exchange"]) for mxRecord in dnsRecord.allMXs()] for dnsRecord in self.dnsRecords.all()]
        return len(allmxs) > 0

    def hasIPV6(self):
        """
        Determine if this Url has a useful IPV6 record
        :return:
        """
        allIpv6s = []
        [allIpv6s.extend(v6Record.allIPV6s()) for v6Record in self.dnsRecords.all()]
        return len(allIpv6s) > 0


class AsnRecord(models.Model):
    """
    Connect an IP address to ASN data. This is connected to an IP address
    as found in a DNS record..

    This model is linked to the URL root model for coherence and lookup.
    """
    url = models.ForeignKey(Url, related_name="asns")
    rawRecord = models.TextField(null=True, blank=True)
    ip = models.GenericIPAddressField(protocol = "IPv4", blank = True, null = True)
    source = models.CharField(max_length=256, null=False, blank=False)

    def formatted(self):
        if self.rawRecord is not None:
            return json.dumps(json.loads(self.rawRecord), indent=4)
        else:
            return ""

class WhoisRecord(models.Model):
    """
    Connect a Whois record for a host to the URL. Linked to the URL root.
    """
    url = models.ForeignKey(Url, related_name="whois")
    rawRecord = models.TextField(null=True, blank=True)

    def formatted(self):
        if self.rawRecord is not None:
            return json.dumps(json.loads(self.rawRecord), indent=4)
        else:
            return ""

class DnsRecord(models.Model):
    """
    Basic representation of DNS resolved data for a Url
    """
    url = models.ForeignKey(Url, related_name="dnsRecords")
    source = models.CharField(max_length=65535, null=False, blank=False)
    rawRecord = models.TextField(null=True, blank=True)

    def formatted(self):
        if self.rawRecord is not None:
            return json.dumps(json.loads(self.rawRecord), indent=4)
        else:
            return ""

    def _formattedRecord(self, recType):
        """
        Extract an individual record type and format it, if it exists
        :param recType:
        :return:
        """
        if self.rawRecord is not None:
            jsonRecord = json.loads(self.rawRecord)
            if recType in jsonRecord:
                #return "\n".join(jsonRecord[recType])
                return jsonRecord[recType][0]
            else:
                return ""
        else:
            return ""

    def formattedA(self):
        return self._formattedRecord("A")

    def formattedAAAA(self):
        return self._formattedRecord("AAAA")

    def formattedNS(self):
        return self._formattedRecord("NS")

    def formattedCNAME(self):
        return self._formattedRecord("CNAME")

    def allMXs(self):
        """
        TODO: Remove after properly implementing the MX record object
        below.
        :return:
        """
        if self.rawRecord is not None:
            jsonRecord = json.loads(self.rawRecord)
            if "MX" in jsonRecord:
                return jsonRecord["MX"]
            else:
                return []
        else:
            return []

    def allIPV6s(self):
        """
        TODO: Remove after properly implementing an IPV6 record object
        :return:
        """
        if self.rawRecord is not None:
            jsonRecord = json.loads(self.rawRecord)
            if "AAAA" in jsonRecord:
                return jsonRecord["AAAA"]
            else:
                return []
        else:
            return []

class MxRecord(models.Model):
    """
    MX Record associated with a DNS entry
    """
    dnsEntry = models.ForeignKey(DnsRecord, related_name="mxRecords")
    priority = models.IntegerField(null=True, blank=True)
    exchange = models.CharField(max_length=65535, null=False, blank=False)