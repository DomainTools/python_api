import os
from domaintools.cli import constants as c


def _iris_investigate_helptext():
    return """
    Returns back a list of domains based on the provided filters. The following filters are available beyond what is parameterized as kwargs: \n
    * --ip: Search for domains having this IP. \n
    * --email: Search for domains with this email in their data. \n
    * --email_domain: Search for domains where the email address uses this domain.\n
    * --nameserver_host: Search for domains with this nameserver.\n
    * --nameserver_domain: Search for domains with a nameserver that has this domain.\n
    * --nameserver_ip: Search for domains with a nameserver on this IP.\n
    * --registrar: Search for domains with this registrar.\n
    * --registrant: Search for domains with this registrant name.\n
    * --registrant_org: Search for domains with this registrant organization.\n
    * --mailserver_host: Search for domains with this mailserver.\n
    * --mailserver_domain: Search for domains with a mailserver that has this domain.\n
    * --mailserver_ip: Search for domains with a mailserver on this IP.\n
    * --redirect_domain: Search for domains which redirect to this domain.\n
    * --ssl_hash: Search for domains which have an SSL certificate with this hash.\n
    * --ssl_subject: Search for domains which have an SSL certificate with this subject string.\n
    * --ssl_email: Search for domains which have an SSL certificate with this email in it.\n
    * --ssl_org: Search for domains which have an SSL certificate with this organization in it.\n
    * --google_analytics: Search for domains which have this Google Analytics code.\n
    * --adsense: Search for domains which have this AdSense code.\n
    * --tld: Filter by TLD. Must be combined with another parameter.\n
    * --search_hash: Use search hash from Iris to bring back domains.\n
    """


def _phisheye_helptext():
    return """
        Returns domain results for the specified term for today or the specified number of days_back. Terms must be setup for monitoring via the web interface: https://research.domaintools.com/phisheye. \n

        NOTE: Properties of a domain are only provided if we have been able to obtain them. \n
        Many domains will have incomplete data because that information isn't available in their Whois records,
        or they don't have DNS results for a name server or IP address.
    """


def _phisheye_termlist():
    return """
        Provides a list of terms that are set up for this account. This call is not charged against your API usage limit.

        NOTE: The terms must be configured in the PhishEye web interface: https://research.domaintools.com/phisheye. \n
        There is no API call to set up the terms.
    """


_command_help_mapper = {
    c.ACCOUNT_INFORMATION: "Provides a snapshot of your accounts current API usage.",
    c.AVAILABLE_API_CALLS: "Provides a list of api calls that you can use based on your account information.",
    c.IRIS_INVESTIGATE: _iris_investigate_helptext(),
    c.IRIS_ENRICH: "Returns back enriched data related to the specified domains using our Iris Enrich service.",
    c.BRAND_MONITOR: "Pass in one or more terms as a list or separated by the pipe character ( | )",
    c.DOMAIN_PROFILE: "Returns a profile for the specified domain name",
    c.DOMAIN_SEARCH: """Each term in the query string must be at least three characters long. Pass in a list or use spaces to separate multiple terms.""",
    c.HOSTING_HISTORY: "Returns the hosting history from the given domain name.",
    c.IP_MONITOR: "Pass in the IP Address you wish to query ( i.e. 199.30.228.112 ).",
    c.IP_REGISTRANT_MONITOR: "Query based on free text query terms",
    c.NAME_SERVER_MONITOR: "Pass in the hostname of the Name Server you wish to query ( i.e. dynect.net ).",
    c.PARSED_WHOIS: "Pass in a domain name.",
    c.REGISTRANT_MONITOR: "One or more terms as a Python list or separated by the pipe character ( | ).",
    c.REPUTATION: "Pass in a domain name to see its reputation score.",
    c.REVERSE_IP: "Pass in a domain name.",
    c.HOST_DOMAINS: "Pass in an IP address.",
    c.REVERSE_IP_WHOIS: "Pass in an IP address or a list of free text query terms.",
    c.REVERSE_NAME_SERVER: "Pass in a domain name or a name server.",
    c.REVERSE_WHOIS: "Provides list of one or more terms to search for in the Whois record, as a Python list or separated with the pipe character ( | ).",
    c.WHOIS: "Pass in a domain name or an IP address to perform a whois lookup.",
    c.WHOIS_HISTORY: "Retrieve historical Whois records of a given domain name.",
    c.PHISHEYE: _phisheye_helptext(),
    c.PHISHEYE_TERM_LIST: _phisheye_termlist(),
    c.IRIS: "Performs a search for the provided search terms ANDed together, returning the pivot engine row data for the resulting domains.",
    c.RISK: "Returns back the risk score for a given domain.",
    c.RISK_EVIDENCE: "Returns back the detailed risk evidence associated with a given domain.",
    c.IRIS_DETECT_MONITORS: "Returns back a list of monitors in Iris Detect based on the provided filters.",
    c.IRIS_DETECT_NEW_DOMAINS: "The Domains endpoint enables users to retrieve details associated with domains for a specific monitor or all monitors.",
    c.IRIS_DETECT_WATCHED_DOMAINS: "Returns back a list of watched domains in Iris Detect based on the provided filters.",
    c.IRIS_DETECT_MANAGE_WATCHLIST_DOMAINS: "Changes the watch state of a list of domains by their Iris Detect domain ID.",
    c.IRIS_DETECT_ESCALATE_DOMAINS: "Changes the escalation type of a list of domains by their Iris Detect domain ID.",
    c.IRIS_DETECT_IGNORED_DOMAINS: "Returns back a list of ignored domains in Iris Detect based on the provided filters.",
}


def get_cli_helptext_by_name(command_name: str) -> str:  # pragma: no cover
    return _command_help_mapper.get(command_name) or ""


def get_file_extension(source: str) -> str:
    ext = os.path.splitext(source)[1]
    return ext


__all__ = ["get_cli_helptext_by_name", "get_file_extension"]
