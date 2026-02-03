#!/usr/bin/env python3
"""
Issue Traffic Generator - Make it look like your computer is having a bad day.

"My WiFi is broken, my computer is slow, and I think I have a virus."
    - Everyone's search history at some point

This module generates realistic traffic patterns that mimic someone
troubleshooting computer, system, network, and adware/malware issues.
Perfect for making your browsing profile look like you're perpetually
fighting with technology.

Inspired by spicy-cat's approach to issue simulation.
"""

__version__ = "1.0.0"
__author__ = "palm-tree"

import asyncio
import random
import time
import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Tuple
from datetime import datetime
from enum import Enum


class IssueType(Enum):
    """
    Types of issues to simulate.

    Each type generates traffic patterns that look like someone
    troubleshooting that specific category of problems.
    """
    # Network Issues
    DNS_FAILURE = "dns_failure"
    CONNECTION_TIMEOUT = "connection_timeout"
    SSL_ERROR = "ssl_error"
    PACKET_LOSS = "packet_loss"
    BANDWIDTH_THROTTLING = "bandwidth_throttling"
    PROXY_ERROR = "proxy_error"
    VPN_ISSUES = "vpn_issues"
    WIFI_PROBLEMS = "wifi_problems"

    # System Issues
    SLOW_COMPUTER = "slow_computer"
    HIGH_CPU = "high_cpu"
    MEMORY_LEAK = "memory_leak"
    DISK_FULL = "disk_full"
    DRIVER_ISSUES = "driver_issues"
    BSOD = "bsod"
    BOOT_FAILURE = "boot_failure"

    # Malware/Adware Issues
    ADWARE_INFECTION = "adware_infection"
    BROWSER_HIJACK = "browser_hijack"
    POPUP_ADS = "popup_ads"
    CRYPTOMINER = "cryptominer"
    RANSOMWARE = "ransomware"
    TROJAN = "trojan"
    SPYWARE = "spyware"

    # Software Issues
    APP_CRASH = "app_crash"
    UPDATE_FAILURE = "update_failure"
    PERMISSION_DENIED = "permission_denied"
    DLL_MISSING = "dll_missing"
    COMPATIBILITY = "compatibility"


@dataclass
class IssuePattern:
    """
    Defines a traffic pattern for a specific issue type.

    "Each problem has its own unique way of making you suffer."
    """
    name: str
    description: str
    search_queries: List[str]
    support_sites: List[str]
    tool_downloads: List[str]
    forum_searches: List[str]
    related_issues: List[str]  # Can chain to other issues
    urgency: float  # 0.0-1.0, affects timing
    frustration_escalation: bool  # Search terms get more desperate over time


# ============================================================================
# ISSUE PATTERN DEFINITIONS
# ============================================================================

ISSUE_PATTERNS: Dict[IssueType, IssuePattern] = {
    # -------------------------------------------------------------------------
    # NETWORK ISSUES
    # -------------------------------------------------------------------------
    IssueType.DNS_FAILURE: IssuePattern(
        name="DNS Resolution Failure",
        description="Can't resolve domain names - the internet is broken",
        search_queries=[
            "dns server not responding",
            "dns_probe_finished_nxdomain",
            "can't resolve hostname",
            "dns lookup failed",
            "server dns address could not be found",
            "dns server unavailable",
            "how to fix dns error",
            "flush dns cache windows",
            "change dns server",
            "best dns servers 2024",
            "dns not working after update",
            "ipconfig /flushdns not working",
            "dns keeps failing",
            "err_name_not_resolved chrome",
            "dns server not responding wifi",
        ],
        support_sites=[
            "https://support.microsoft.com/en-us/windows/fix-dns-issues",
            "https://support.google.com/chrome/answer/95669",
            "https://www.cloudflare.com/learning/dns/what-is-dns/",
            "https://www.howtogeek.com/167533/the-ultimate-guide-to-changing-your-dns-server/",
            "https://www.lifewire.com/how-to-change-dns-server-settings-2617979",
        ],
        tool_downloads=[
            "https://www.nirsoft.net/utils/dns_query_sniffer.html",
            "https://sourceforge.net/projects/dnsdataview/",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=dns+not+working",
            "https://superuser.com/questions/tagged/dns",
            "https://answers.microsoft.com/en-us/search?query=dns+server",
        ],
        related_issues=["wifi_problems", "connection_timeout"],
        urgency=0.8,
        frustration_escalation=True,
    ),

    IssueType.CONNECTION_TIMEOUT: IssuePattern(
        name="Connection Timeout",
        description="Requests timing out - is the internet even real?",
        search_queries=[
            "connection timed out",
            "err_connection_timed_out",
            "request timeout error",
            "website not loading timeout",
            "connection timeout how to fix",
            "chrome connection timeout",
            "internet connected but pages won't load",
            "increase connection timeout",
            "tcp connection timeout",
            "server not responding timeout",
            "fix timeout errors windows",
            "why do websites keep timing out",
            "connection timeout vs connection refused",
        ],
        support_sites=[
            "https://support.google.com/chrome/answer/95669",
            "https://www.lifewire.com/fix-err-connection-timed-out-5179936",
            "https://www.hostinger.com/tutorials/err-connection-timed-out",
        ],
        tool_downloads=[
            "https://www.speedtest.net",
            "https://fast.com",
            "https://www.meter.net",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=connection+timeout",
            "https://superuser.com/questions/tagged/timeout",
        ],
        related_issues=["dns_failure", "packet_loss", "proxy_error"],
        urgency=0.7,
        frustration_escalation=True,
    ),

    IssueType.SSL_ERROR: IssuePattern(
        name="SSL/TLS Certificate Error",
        description="Certificate problems - trust issues with the internet",
        search_queries=[
            "ssl certificate error",
            "your connection is not private",
            "err_cert_authority_invalid",
            "ssl handshake failed",
            "certificate expired error",
            "net::err_cert_date_invalid",
            "ssl certificate problem",
            "how to bypass ssl error",
            "fix ssl certificate error chrome",
            "ssl_error_rx_record_too_long",
            "certificate not trusted",
            "self signed certificate error",
            "ssl certificate verify failed",
            "https not secure warning",
        ],
        support_sites=[
            "https://support.google.com/chrome/answer/6098869",
            "https://www.ssl.com/faqs/what-is-an-ssl-certificate/",
            "https://letsencrypt.org/docs/",
            "https://www.digicert.com/help/",
        ],
        tool_downloads=[
            "https://www.ssllabs.com/ssltest/",
            "https://whatsmychainsert.com",
        ],
        forum_searches=[
            "https://stackoverflow.com/questions/tagged/ssl-certificate",
            "https://security.stackexchange.com/questions/tagged/tls",
        ],
        related_issues=["proxy_error", "connection_timeout"],
        urgency=0.6,
        frustration_escalation=False,
    ),

    IssueType.PACKET_LOSS: IssuePattern(
        name="Packet Loss",
        description="Data disappearing into the void",
        search_queries=[
            "packet loss test",
            "high packet loss fix",
            "packet loss gaming",
            "why am i getting packet loss",
            "packet loss router",
            "reduce packet loss",
            "packet loss wifi",
            "0% packet loss but high ping",
            "packet loss spikes",
            "network packet loss troubleshooting",
            "packet loss cmd test",
            "tracert shows packet loss",
            "is packet loss bad",
            "acceptable packet loss percentage",
        ],
        support_sites=[
            "https://www.speedtest.net/insights/blog/how-to-test-packet-loss/",
            "https://www.lifewire.com/packet-loss-1847879",
            "https://www.cloudflare.com/learning/network-layer/what-is-packet-loss/",
        ],
        tool_downloads=[
            "https://www.pingplotter.com",
            "https://sourceforge.net/projects/winmtr/",
        ],
        forum_searches=[
            "https://www.reddit.com/r/HomeNetworking/search?q=packet+loss",
            "https://superuser.com/questions/tagged/packet-loss",
        ],
        related_issues=["wifi_problems", "bandwidth_throttling"],
        urgency=0.6,
        frustration_escalation=True,
    ),

    IssueType.WIFI_PROBLEMS: IssuePattern(
        name="WiFi Connectivity Issues",
        description="The WiFi is doing that thing again",
        search_queries=[
            "wifi keeps disconnecting",
            "wifi connected but no internet",
            "wifi not working windows 11",
            "wifi slow on my computer only",
            "wifi adapter not showing",
            "reset wifi adapter",
            "wifi authentication problem",
            "wifi driver windows 11",
            "wifi signal weak fix",
            "5ghz wifi not showing",
            "wifi keeps dropping",
            "forget wifi network",
            "wifi connected no internet android",
            "why does my wifi suck",
            "wifi extender not working",
        ],
        support_sites=[
            "https://support.microsoft.com/en-us/windows/fix-wi-fi-connection-issues-in-windows",
            "https://support.apple.com/en-us/HT210060",
            "https://www.intel.com/content/www/us/en/support/articles/000005489/wireless.html",
            "https://www.lifewire.com/troubleshooting-no-wireless-connection-2378241",
        ],
        tool_downloads=[
            "https://www.nirsoft.net/utils/wireless_network_watcher.html",
            "https://www.netspotapp.com",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=wifi+not+working",
            "https://www.reddit.com/r/HomeNetworking/search?q=wifi+issues",
            "https://answers.microsoft.com/en-us/search?query=wifi+problems",
        ],
        related_issues=["dns_failure", "connection_timeout", "driver_issues"],
        urgency=0.8,
        frustration_escalation=True,
    ),

    IssueType.VPN_ISSUES: IssuePattern(
        name="VPN Connection Problems",
        description="VPN won't connect - privacy at stake",
        search_queries=[
            "vpn not connecting",
            "vpn connection failed",
            "vpn keeps disconnecting",
            "vpn slow speed",
            "vpn blocked by firewall",
            "openvpn connection refused",
            "wireguard handshake timeout",
            "nordvpn not working",
            "expressvpn connection issues",
            "vpn authentication failed",
            "ipsec vpn troubleshooting",
            "vpn no internet access",
            "split tunneling vpn",
            "vpn dns leak",
        ],
        support_sites=[
            "https://support.nordvpn.com",
            "https://www.expressvpn.com/support/",
            "https://openvpn.net/community-resources/",
            "https://www.wireguard.com/quickstart/",
        ],
        tool_downloads=[
            "https://www.dnsleaktest.com",
            "https://ipleak.net",
        ],
        forum_searches=[
            "https://www.reddit.com/r/VPN/search?q=not+connecting",
            "https://superuser.com/questions/tagged/vpn",
        ],
        related_issues=["proxy_error", "dns_failure", "ssl_error"],
        urgency=0.7,
        frustration_escalation=True,
    ),

    IssueType.PROXY_ERROR: IssuePattern(
        name="Proxy Configuration Error",
        description="Proxy settings are haunted",
        search_queries=[
            "proxy server not responding",
            "unable to connect to proxy server",
            "err_proxy_connection_failed",
            "check proxy settings",
            "proxy server refusing connections",
            "how to disable proxy",
            "automatic proxy detection failed",
            "pac file not working",
            "corporate proxy bypass",
            "proxy authentication required",
            "clear proxy settings windows",
            "internet explorer proxy settings",
        ],
        support_sites=[
            "https://support.microsoft.com/en-us/windows/use-a-proxy-server-in-windows",
            "https://www.lifewire.com/disable-proxy-settings-4153918",
        ],
        tool_downloads=[],
        forum_searches=[
            "https://superuser.com/questions/tagged/proxy",
            "https://stackoverflow.com/questions/tagged/proxy",
        ],
        related_issues=["connection_timeout", "ssl_error"],
        urgency=0.5,
        frustration_escalation=False,
    ),

    # -------------------------------------------------------------------------
    # SYSTEM ISSUES
    # -------------------------------------------------------------------------
    IssueType.SLOW_COMPUTER: IssuePattern(
        name="Slow Computer Performance",
        description="Computer running like it's 1999",
        search_queries=[
            "why is my computer so slow",
            "speed up windows 11",
            "computer running slow fix",
            "pc slow after update",
            "how to make laptop faster",
            "100% disk usage windows",
            "clean up computer",
            "disable startup programs",
            "computer freezing randomly",
            "windows 11 performance issues",
            "ssd slow suddenly",
            "pc takes forever to boot",
            "system interrupts high cpu",
            "computer slow all of a sudden",
            "is 8gb ram enough 2024",
        ],
        support_sites=[
            "https://support.microsoft.com/en-us/windows/tips-to-improve-pc-performance-in-windows",
            "https://www.avg.com/en/signal/speed-up-computer",
            "https://www.pcmag.com/how-to/speed-up-windows",
        ],
        tool_downloads=[
            "https://www.ccleaner.com",
            "https://www.malwarebytes.com",
            "https://crystalmark.info/en/software/crystaldiskinfo/",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=computer+slow",
            "https://superuser.com/questions/tagged/performance",
            "https://answers.microsoft.com/en-us/search?query=slow+computer",
        ],
        related_issues=["high_cpu", "memory_leak", "disk_full", "adware_infection"],
        urgency=0.6,
        frustration_escalation=True,
    ),

    IssueType.HIGH_CPU: IssuePattern(
        name="High CPU Usage",
        description="CPU running hotter than the sun",
        search_queries=[
            "100% cpu usage windows",
            "high cpu usage fix",
            "what is using my cpu",
            "system idle process high cpu",
            "svchost high cpu",
            "wmi provider host high cpu",
            "antimalware service executable high cpu",
            "chrome high cpu usage",
            "cpu usage spikes to 100",
            "how to reduce cpu usage",
            "cpu always at 100",
            "task manager cpu usage wrong",
            "desktop window manager high cpu",
            "wsappx high cpu",
        ],
        support_sites=[
            "https://support.microsoft.com/en-us/windows/fix-high-cpu-usage",
            "https://www.lifewire.com/fix-high-cpu-usage-windows-4584988",
            "https://www.howtogeek.com/howto/windows-vista/what-is-svchostexe-and-why-is-it-running/",
        ],
        tool_downloads=[
            "https://docs.microsoft.com/en-us/sysinternals/downloads/process-explorer",
            "https://www.cpuid.com/softwares/hwmonitor.html",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=high+cpu",
            "https://superuser.com/questions/tagged/cpu-usage",
        ],
        related_issues=["slow_computer", "cryptominer", "memory_leak"],
        urgency=0.7,
        frustration_escalation=True,
    ),

    IssueType.MEMORY_LEAK: IssuePattern(
        name="Memory Leak",
        description="RAM being consumed by the void",
        search_queries=[
            "memory leak windows",
            "high memory usage fix",
            "ram usage 100%",
            "find memory leak windows",
            "chrome using too much memory",
            "memory leak detection",
            "non-paged pool memory leak",
            "system using too much ram",
            "memory leak symptoms",
            "windows memory leak driver",
            "how to fix memory leak",
            "standby memory too high",
            "ram always full",
            "what is eating my ram",
        ],
        support_sites=[
            "https://support.microsoft.com/en-us/windows/fix-memory-problems",
            "https://www.lifewire.com/fix-memory-leak-windows-4692717",
        ],
        tool_downloads=[
            "https://docs.microsoft.com/en-us/sysinternals/downloads/rammap",
            "https://www.memtest.org",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=memory+leak",
            "https://superuser.com/questions/tagged/memory-leak",
        ],
        related_issues=["high_cpu", "slow_computer"],
        urgency=0.6,
        frustration_escalation=True,
    ),

    IssueType.DISK_FULL: IssuePattern(
        name="Disk Space Full",
        description="Where did all the storage go?",
        search_queries=[
            "disk space full",
            "c drive full",
            "free up disk space windows",
            "what is taking up space on my hard drive",
            "low disk space warning",
            "winsxs folder huge",
            "windows.old delete",
            "clear temp files windows",
            "disk cleanup",
            "can i delete system volume information",
            "hiberfil.sys delete",
            "pagefile.sys too big",
            "storage sense windows",
            "find large files windows",
        ],
        support_sites=[
            "https://support.microsoft.com/en-us/windows/free-up-drive-space-in-windows",
            "https://www.howtogeek.com/125923/7-ways-to-free-up-hard-disk-space-on-windows/",
        ],
        tool_downloads=[
            "https://windirstat.net",
            "https://www.jam-software.com/treesize_free",
            "https://sourceforge.net/projects/bleachbit/",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=disk+full",
            "https://superuser.com/questions/tagged/disk-space",
        ],
        related_issues=["slow_computer", "update_failure"],
        urgency=0.7,
        frustration_escalation=True,
    ),

    IssueType.BSOD: IssuePattern(
        name="Blue Screen of Death",
        description="The dreaded BSOD",
        search_queries=[
            "blue screen of death fix",
            "bsod windows 11",
            "irql_not_less_or_equal",
            "system_service_exception",
            "kernel_security_check_failure",
            "page_fault_in_nonpaged_area",
            "critical_process_died",
            "memory_management bsod",
            "dpc_watchdog_violation",
            "whea_uncorrectable_error",
            "analyze minidump",
            "bsod after windows update",
            "blue screen keeps happening",
            "stop code windows",
            "bsod viewer",
        ],
        support_sites=[
            "https://support.microsoft.com/en-us/windows/troubleshoot-blue-screen-errors",
            "https://www.lifewire.com/how-to-fix-a-blue-screen-of-death-2624518",
            "https://www.bleepingcomputer.com/forums/f/167/windows-crashes-and-blue-screen-of-death-bsod-help-and-support/",
        ],
        tool_downloads=[
            "https://www.nirsoft.net/utils/blue_screen_view.html",
            "https://www.nirsoft.net/utils/win_crash_dump.html",
            "https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=blue+screen",
            "https://answers.microsoft.com/en-us/search?query=BSOD",
            "https://www.tenforums.com/bsod-crashes-debugging/",
        ],
        related_issues=["driver_issues", "memory_leak", "high_cpu"],
        urgency=0.9,
        frustration_escalation=True,
    ),

    IssueType.DRIVER_ISSUES: IssuePattern(
        name="Driver Problems",
        description="Drivers refusing to cooperate",
        search_queries=[
            "driver update windows",
            "device driver error",
            "driver not installed",
            "driver verifier detected violation",
            "code 43 graphics card",
            "nvidia driver not installing",
            "amd driver crash",
            "audio driver not working",
            "usb driver error",
            "rollback driver",
            "driver signature enforcement disable",
            "update drivers automatically",
            "driver booster safe",
            "device manager yellow triangle",
        ],
        support_sites=[
            "https://support.microsoft.com/en-us/windows/update-drivers-manually-in-windows",
            "https://www.nvidia.com/Download/index.aspx",
            "https://www.amd.com/en/support",
            "https://www.intel.com/content/www/us/en/support/detect.html",
        ],
        tool_downloads=[
            "https://www.nvidia.com/en-us/geforce/geforce-experience/",
            "https://sdi-tool.org",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=driver+problem",
            "https://superuser.com/questions/tagged/drivers",
        ],
        related_issues=["bsod", "wifi_problems", "slow_computer"],
        urgency=0.7,
        frustration_escalation=True,
    ),

    # -------------------------------------------------------------------------
    # MALWARE/ADWARE ISSUES
    # -------------------------------------------------------------------------
    IssueType.ADWARE_INFECTION: IssuePattern(
        name="Adware Infection",
        description="Ads everywhere - browser is infected",
        search_queries=[
            "remove adware",
            "popup ads virus",
            "ads on every website",
            "browser has adware",
            "how to get rid of adware",
            "adware removal tool",
            "chrome infected with ads",
            "random popups on computer",
            "adware scan",
            "malwarebytes adware",
            "browser redirect virus",
            "unwanted ads appearing",
            "sponsored ads virus",
            "notification spam remove",
        ],
        support_sites=[
            "https://www.malwarebytes.com/adware",
            "https://www.avg.com/en/signal/what-is-adware",
            "https://support.google.com/chrome/answer/2765944",
            "https://www.bleepingcomputer.com/virus-removal/",
        ],
        tool_downloads=[
            "https://www.malwarebytes.com/adwcleaner",
            "https://www.bitdefender.com/solutions/free.html",
            "https://www.kaspersky.com/free-virus-scanner",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=adware",
            "https://www.bleepingcomputer.com/forums/f/22/virus-trojan-spyware-and-malware-removal-help/",
        ],
        related_issues=["browser_hijack", "popup_ads", "slow_computer"],
        urgency=0.8,
        frustration_escalation=True,
    ),

    IssueType.BROWSER_HIJACK: IssuePattern(
        name="Browser Hijack",
        description="Browser taken over by malicious software",
        search_queries=[
            "browser hijacked",
            "homepage changed virus",
            "search engine changed to yahoo",
            "bing redirect virus",
            "browser redirect malware",
            "new tab opens random sites",
            "reset browser hijack",
            "chrome hijacked",
            "default search engine keeps changing",
            "suspicious browser extension",
            "remove browser hijacker",
            "firefox homepage changed",
            "trovi removal",
            "conduit search remove",
        ],
        support_sites=[
            "https://support.google.com/chrome/answer/2765944",
            "https://support.mozilla.org/en-US/kb/remove-toolbar-has-taken-over-your-firefox-search",
            "https://www.malwarebytes.com/browser-hijacker",
        ],
        tool_downloads=[
            "https://www.malwarebytes.com",
            "https://www.hitmanpro.com",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=browser+hijack",
            "https://www.bleepingcomputer.com/forums/",
        ],
        related_issues=["adware_infection", "popup_ads", "spyware"],
        urgency=0.8,
        frustration_escalation=True,
    ),

    IssueType.POPUP_ADS: IssuePattern(
        name="Unwanted Popup Ads",
        description="Popups appearing from nowhere",
        search_queries=[
            "stop popup ads",
            "popup ads won't stop",
            "random popups on desktop",
            "notification popup virus",
            "chrome popup ads",
            "popup blocker not working",
            "mcafee popup scam",
            "windows defender popup fake",
            "tech support popup scam",
            "website notification spam",
            "how to disable chrome notifications",
            "malicious popups",
            "popup ads corner screen",
            "edge notifications spam",
        ],
        support_sites=[
            "https://support.google.com/chrome/answer/3220216",
            "https://support.microsoft.com/en-us/microsoft-edge/block-pop-ups-in-microsoft-edge",
            "https://www.malwarebytes.com/pop-ups",
        ],
        tool_downloads=[
            "https://www.malwarebytes.com",
            "https://adblockplus.org",
            "https://ublockorigin.com",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=popup+ads",
            "https://superuser.com/questions/tagged/popup",
        ],
        related_issues=["adware_infection", "browser_hijack"],
        urgency=0.7,
        frustration_escalation=True,
    ),

    IssueType.CRYPTOMINER: IssuePattern(
        name="Cryptominer Malware",
        description="Computer mining crypto without permission",
        search_queries=[
            "computer mining bitcoin virus",
            "cpu 100% cryptominer",
            "coinhive detection",
            "cryptominer removal",
            "browser mining malware",
            "gpu usage high when idle",
            "fan running high for no reason",
            "crypto malware scan",
            "monero miner virus",
            "detect cryptojacking",
            "remove coin miner",
            "powershell.exe high cpu miner",
            "cryptomining malware symptoms",
        ],
        support_sites=[
            "https://www.malwarebytes.com/cryptojacking",
            "https://www.kaspersky.com/resource-center/threats/cryptominers",
            "https://www.bleepingcomputer.com/tag/cryptocurrency-miner/",
        ],
        tool_downloads=[
            "https://www.malwarebytes.com",
            "https://www.emsisoft.com/en/",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=cryptominer",
            "https://www.reddit.com/r/antivirus/search?q=crypto+miner",
        ],
        related_issues=["high_cpu", "slow_computer", "trojan"],
        urgency=0.8,
        frustration_escalation=True,
    ),

    IssueType.RANSOMWARE: IssuePattern(
        name="Ransomware Attack",
        description="Files encrypted - paying ransom?",
        search_queries=[
            "ransomware help",
            "files encrypted virus",
            "ransomware decryption tool",
            "how to recover encrypted files",
            "ransomware removal",
            "stop ransomware",
            "no more ransom",
            "ransomware file recovery",
            "should i pay ransomware",
            "decrypt files without paying",
            "id ransomware",
            "ransomware extensions",
            "backup after ransomware",
            "ransomware prevention",
        ],
        support_sites=[
            "https://www.nomoreransom.org",
            "https://www.malwarebytes.com/ransomware",
            "https://www.cisa.gov/stopransomware",
            "https://www.kaspersky.com/resource-center/threats/ransomware",
        ],
        tool_downloads=[
            "https://www.nomoreransom.org/en/decryption-tools.html",
            "https://www.emsisoft.com/ransomware-decryption-tools/",
            "https://www.avg.com/en-us/ransomware-decryption-tools",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=ransomware",
            "https://www.bleepingcomputer.com/forums/f/239/ransomware-help-tech-support/",
        ],
        related_issues=["trojan", "spyware"],
        urgency=1.0,
        frustration_escalation=True,
    ),

    IssueType.TROJAN: IssuePattern(
        name="Trojan Infection",
        description="Trojan horse detected",
        search_queries=[
            "trojan virus removal",
            "trojan detected windows defender",
            "trojan:win32 removal",
            "how to remove trojan",
            "trojan horse virus",
            "backdoor trojan",
            "remote access trojan",
            "trojan downloader",
            "trojan generic detection",
            "is trojan dangerous",
            "computer has trojan",
            "trojan scan",
            "remove trojan manually",
            "trojan keeps coming back",
        ],
        support_sites=[
            "https://www.malwarebytes.com/trojan",
            "https://www.avg.com/en/signal/what-is-a-trojan",
            "https://support.microsoft.com/en-us/windows/protect-your-pc-from-ransomware",
        ],
        tool_downloads=[
            "https://www.malwarebytes.com",
            "https://www.kaspersky.com/free-virus-scanner",
            "https://www.eset.com/us/home/online-scanner/",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=trojan",
            "https://www.bleepingcomputer.com/forums/",
        ],
        related_issues=["spyware", "cryptominer", "ransomware"],
        urgency=0.9,
        frustration_escalation=True,
    ),

    IssueType.SPYWARE: IssuePattern(
        name="Spyware Detection",
        description="Something is watching",
        search_queries=[
            "spyware removal",
            "computer spying on me",
            "detect spyware",
            "keylogger detection",
            "is someone monitoring my computer",
            "remove spyware windows",
            "anti spyware software",
            "spyware scan free",
            "stalkerware removal",
            "screen monitoring software detect",
            "webcam spyware",
            "someone watching my screen",
            "employer monitoring software detect",
            "find hidden spy software",
        ],
        support_sites=[
            "https://www.malwarebytes.com/spyware",
            "https://www.avg.com/en/signal/what-is-spyware",
            "https://www.eff.org/deeplinks/2020/06/detect-stalkerware-your-devices",
        ],
        tool_downloads=[
            "https://www.malwarebytes.com",
            "https://www.spybot.info",
            "https://www.superantispyware.com",
        ],
        forum_searches=[
            "https://www.reddit.com/r/techsupport/search?q=spyware",
            "https://www.reddit.com/r/privacy/search?q=stalkerware",
        ],
        related_issues=["trojan", "browser_hijack", "adware_infection"],
        urgency=0.9,
        frustration_escalation=True,
    ),

    # -------------------------------------------------------------------------
    # SOFTWARE ISSUES
    # -------------------------------------------------------------------------
    IssueType.APP_CRASH: IssuePattern(
        name="Application Crash",
        description="Apps keep crashing",
        search_queries=[
            "application keeps crashing",
            "program stopped working",
            "app crash fix",
            "program freezes then closes",
            "application error windows",
            "app crashing on startup",
            "event viewer application error",
            "memory could not be read",
            "exception access violation",
            "application hang",
            "program not responding",
            "force close application",
            "crash dump analysis",
        ],
        support_sites=[
            "https://support.microsoft.com/en-us/windows/troubleshoot-app-problems",
            "https://www.howtogeek.com/222730/how-to-find-out-why-a-program-crashed-using-windows-event-viewer/",
        ],
        tool_downloads=[
            "https://docs.microsoft.com/en-us/sysinternals/downloads/process-monitor",
            "https://www.nirsoft.net/utils/app_crash_view.html",
        ],
        forum_searches=[
            "https://superuser.com/questions/tagged/crash",
            "https://www.reddit.com/r/techsupport/search?q=app+crash",
        ],
        related_issues=["dll_missing", "compatibility", "driver_issues"],
        urgency=0.6,
        frustration_escalation=True,
    ),

    IssueType.UPDATE_FAILURE: IssuePattern(
        name="Update Failure",
        description="Windows update stuck or failing",
        search_queries=[
            "windows update failed",
            "update stuck at 100%",
            "windows update error",
            "update error 0x80070002",
            "windows update not working",
            "update download stuck",
            "reset windows update",
            "update troubleshooter",
            "pending updates won't install",
            "windows update service missing",
            "sfc /scannow update",
            "dism repair windows update",
            "force windows update",
            "clean boot for updates",
        ],
        support_sites=[
            "https://support.microsoft.com/en-us/windows/troubleshoot-problems-updating-windows",
            "https://www.howtogeek.com/247380/how-to-fix-windows-update-when-it-gets-stuck/",
        ],
        tool_downloads=[
            "https://support.microsoft.com/en-us/topic/windows-update-troubleshooter-19bc41d4-eb57-4ea8-8d3c-6bf51f6ff729",
        ],
        forum_searches=[
            "https://www.reddit.com/r/Windows10/search?q=update+failed",
            "https://answers.microsoft.com/en-us/search?query=update+error",
        ],
        related_issues=["disk_full", "slow_computer"],
        urgency=0.6,
        frustration_escalation=True,
    ),

    IssueType.DLL_MISSING: IssuePattern(
        name="DLL Missing Error",
        description="DLL file not found",
        search_queries=[
            "dll file missing",
            "msvcp140.dll missing",
            "vcruntime140.dll not found",
            "api-ms-win missing",
            "download missing dll",
            "reinstall visual c++",
            "dll error windows",
            "system32 dll missing",
            "d3dx9 dll download",
            "xinput1_4.dll missing",
            "is dll download safe",
            "register dll windows",
            "dll hell fix",
            "visual c++ redistributable all versions",
        ],
        support_sites=[
            "https://support.microsoft.com/en-us/windows/fix-missing-dll-errors",
            "https://www.howtogeek.com/326207/how-to-fix-missing-dll-file-errors-on-windows/",
            "https://www.microsoft.com/en-us/download/details.aspx?id=48145",
        ],
        tool_downloads=[
            "https://www.microsoft.com/en-us/download/details.aspx?id=48145",
            "https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads",
        ],
        forum_searches=[
            "https://superuser.com/questions/tagged/dll",
            "https://www.reddit.com/r/techsupport/search?q=dll+missing",
        ],
        related_issues=["app_crash", "update_failure"],
        urgency=0.5,
        frustration_escalation=False,
    ),

    IssueType.COMPATIBILITY: IssuePattern(
        name="Compatibility Issues",
        description="Software compatibility problems",
        search_queries=[
            "compatibility mode windows",
            "program not compatible windows 11",
            "run old software windows 10",
            "this app can't run on your pc",
            "compatibility troubleshooter",
            "32 bit on 64 bit",
            "legacy software windows",
            "program compatibility settings",
            "windows xp mode",
            "dosbox setup",
            "wine windows apps",
            "virtual machine old software",
            "run as administrator compatibility",
        ],
        support_sites=[
            "https://support.microsoft.com/en-us/windows/make-older-apps-or-programs-compatible-with-windows-10",
            "https://www.howtogeek.com/228689/how-to-make-old-programs-work-on-windows-10/",
        ],
        tool_downloads=[
            "https://www.dosbox.com",
            "https://www.virtualbox.org",
        ],
        forum_searches=[
            "https://superuser.com/questions/tagged/compatibility",
            "https://www.reddit.com/r/techsupport/search?q=compatibility",
        ],
        related_issues=["app_crash", "driver_issues"],
        urgency=0.4,
        frustration_escalation=False,
    ),
}


# ============================================================================
# TRAFFIC GENERATOR CLASS
# ============================================================================

class IssueTrafficGenerator:
    """
    Generates realistic traffic patterns mimicking troubleshooting behavior.

    "Making your browsing history look like you're perpetually fighting
    with technology."

    This is designed to look like genuine troubleshooting behavior:
    - Search queries become more desperate over time
    - Related issues can cascade (one problem leads to searching for another)
    - Timing mimics frustrated user behavior
    """

    def __init__(
        self,
        issue_types: Optional[List[IssueType]] = None,
        fetch_callback: Optional[Callable] = None,
        frustration_mode: bool = True,
        chaos_factor: float = 0.3,
    ):
        """
        Initialize the issue traffic generator.

        Args:
            issue_types: List of issue types to simulate (None = random selection)
            fetch_callback: Async function to call for each URL (receives url, category)
            frustration_mode: Enable escalating search desperation
            chaos_factor: Probability of jumping to related issues (0.0-1.0)
        """
        self.issue_types = issue_types or list(IssueType)
        self.fetch_callback = fetch_callback
        self.frustration_mode = frustration_mode
        self.chaos_factor = chaos_factor

        self.running = False
        self.current_issue: Optional[IssueType] = None
        self.search_count = 0
        self.total_requests = 0

        # Stats
        self.stats = {
            "issues_simulated": {},
            "total_searches": 0,
            "total_requests": 0,
            "frustration_escalations": 0,
            "issue_chains": 0,
            "start_time": None,
        }

    def _get_search_url(self, query: str, engine: str = "google") -> str:
        """Build a search URL for the given query."""
        encoded_query = query.replace(" ", "+")

        engines = {
            "google": f"https://www.google.com/search?q={encoded_query}",
            "bing": f"https://www.bing.com/search?q={encoded_query}",
            "duckduckgo": f"https://duckduckgo.com/?q={encoded_query}",
            "reddit": f"https://www.reddit.com/search/?q={encoded_query}",
            "youtube": f"https://www.youtube.com/results?search_query={encoded_query}",
        }

        return engines.get(engine, engines["google"])

    def _select_issue(self) -> IssueType:
        """Select an issue type to simulate."""
        if self.current_issue and random.random() < self.chaos_factor:
            # Check for related issues
            pattern = ISSUE_PATTERNS[self.current_issue]
            related = [r for r in pattern.related_issues if IssueType(r) in self.issue_types]
            if related:
                related_type = IssueType(random.choice(related))
                self.stats["issue_chains"] += 1
                print(f"[IssueTraffic] Issue chain: {self.current_issue.value} -> {related_type.value}")
                return related_type

        return random.choice(self.issue_types)

    def _get_delay(self, urgency: float) -> float:
        """
        Calculate delay based on urgency and frustration.

        Higher urgency = shorter delays (frantic searching)
        Frustration mode = delays decrease over time
        """
        base_delay = random.uniform(3, 15)

        # Urgency factor (higher urgency = faster)
        urgency_multiplier = 1.0 - (urgency * 0.7)

        # Frustration factor (more searches = more frantic)
        if self.frustration_mode and self.search_count > 5:
            frustration_multiplier = max(0.3, 1.0 - (self.search_count * 0.05))
            self.stats["frustration_escalations"] += 1
        else:
            frustration_multiplier = 1.0

        # Add some chaos
        chaos = random.uniform(0.5, 1.5)

        return base_delay * urgency_multiplier * frustration_multiplier * chaos

    def _modify_query_for_frustration(self, query: str, search_num: int) -> str:
        """Make search queries more desperate over time."""
        if not self.frustration_mode or search_num < 3:
            return query

        frustration_prefixes = [
            "", "", "",  # Often no prefix
            "how to fix ",
            "why ",
            "help ",
            "please help ",
            "still ",
            "urgent ",
        ]

        frustration_suffixes = [
            "", "", "",  # Often no suffix
            " fix",
            " solution",
            " not working",
            " still not working",
            " please help",
            " driving me crazy",
            " reddit",
            " 2024",
        ]

        # Escalate based on search count
        if search_num > 10:
            # Really frustrated
            prefix = random.choice(["please help ", "urgent ", "HELP ", ""])
            suffix = random.choice([" not working", " STILL broken", " nothing works", ""])
        elif search_num > 5:
            prefix = random.choice(frustration_prefixes)
            suffix = random.choice(frustration_suffixes)
        else:
            prefix = ""
            suffix = random.choice(["", "", " fix", " solution"])

        return f"{prefix}{query}{suffix}".strip()

    async def _visit_url(self, url: str, category: str, issue_type: str):
        """Visit a URL (via callback or just log)."""
        self.total_requests += 1
        self.stats["total_requests"] += 1

        if self.fetch_callback:
            try:
                await self.fetch_callback(url, category=category, issue_type=issue_type)
            except Exception as e:
                print(f"[IssueTraffic] Fetch error: {e}")
        else:
            print(f"[IssueTraffic] [{issue_type}] {category}: {url[:60]}...")

    async def simulate_issue(self, issue_type: IssueType, duration_seconds: int = 300):
        """
        Simulate troubleshooting a specific issue.

        This creates a realistic sequence of:
        1. Initial search queries
        2. Visiting support sites
        3. Forum searching
        4. Tool downloads
        5. More desperate searches (if frustration mode)
        """
        pattern = ISSUE_PATTERNS[issue_type]
        self.current_issue = issue_type
        self.search_count = 0

        print(f"\n[IssueTraffic] Simulating: {pattern.name}")
        print(f"[IssueTraffic] Description: {pattern.description}")

        # Track this issue
        if issue_type.value not in self.stats["issues_simulated"]:
            self.stats["issues_simulated"][issue_type.value] = 0
        self.stats["issues_simulated"][issue_type.value] += 1

        end_time = time.time() + duration_seconds

        while self.running and time.time() < end_time:
            self.search_count += 1
            self.stats["total_searches"] += 1

            # Decide what action to take
            action = random.choices(
                ["search", "support", "forum", "tool", "youtube"],
                weights=[0.4, 0.25, 0.2, 0.1, 0.05],
                k=1
            )[0]

            if action == "search":
                # Search query
                query = random.choice(pattern.search_queries)
                query = self._modify_query_for_frustration(query, self.search_count)
                engine = random.choices(
                    ["google", "bing", "duckduckgo"],
                    weights=[0.7, 0.2, 0.1],
                    k=1
                )[0]
                url = self._get_search_url(query, engine)
                await self._visit_url(url, f"search_{engine}", issue_type.value)

            elif action == "support" and pattern.support_sites:
                # Visit support site
                url = random.choice(pattern.support_sites)
                await self._visit_url(url, "support_site", issue_type.value)

            elif action == "forum" and pattern.forum_searches:
                # Visit forum
                url = random.choice(pattern.forum_searches)
                await self._visit_url(url, "forum", issue_type.value)

            elif action == "tool" and pattern.tool_downloads:
                # Visit tool download page
                url = random.choice(pattern.tool_downloads)
                await self._visit_url(url, "tool_download", issue_type.value)

            elif action == "youtube":
                # Search YouTube for fix
                query = random.choice(pattern.search_queries)
                url = self._get_search_url(f"fix {query}", "youtube")
                await self._visit_url(url, "youtube", issue_type.value)

            # Delay before next action
            delay = self._get_delay(pattern.urgency)
            await asyncio.sleep(delay)

            # Chance to switch to related issue
            if pattern.related_issues and random.random() < self.chaos_factor * 0.5:
                break

    async def run(
        self,
        duration_minutes: int = 60,
        issues_per_session: int = 3,
    ):
        """
        Run the issue traffic generator.

        Args:
            duration_minutes: Total duration to run
            issues_per_session: Number of different issues to simulate
        """
        self.running = True
        self.stats["start_time"] = datetime.now()

        print("\n" + "=" * 60)
        print("ISSUE TRAFFIC GENERATOR - Making Tech Support Look Realistic")
        print("=" * 60)
        print(f"Duration: {duration_minutes} minutes")
        print(f"Issues per session: {issues_per_session}")
        print(f"Frustration mode: {'ON' if self.frustration_mode else 'OFF'}")
        print(f"Chaos factor: {self.chaos_factor}")
        print("=" * 60 + "\n")

        end_time = time.time() + (duration_minutes * 60)
        issues_simulated = 0

        while self.running and time.time() < end_time:
            # Select an issue to simulate
            issue_type = self._select_issue()

            # Calculate duration for this issue
            remaining = end_time - time.time()
            issue_duration = min(
                random.uniform(60, 300),  # 1-5 minutes per issue
                remaining
            )

            if issue_duration < 30:  # Less than 30 seconds left
                break

            await self.simulate_issue(issue_type, int(issue_duration))
            issues_simulated += 1

            # Brief pause between issues
            if self.running and time.time() < end_time:
                await asyncio.sleep(random.uniform(5, 15))

        self.running = False
        self._print_stats()

    def stop(self):
        """Stop the generator."""
        self.running = False

    def _print_stats(self):
        """Print session statistics."""
        print("\n" + "=" * 60)
        print("ISSUE TRAFFIC SESSION COMPLETE")
        print("=" * 60)
        print(f"Total requests: {self.stats['total_requests']}")
        print(f"Total searches: {self.stats['total_searches']}")
        print(f"Issues simulated: {len(self.stats['issues_simulated'])}")
        print(f"Frustration escalations: {self.stats['frustration_escalations']}")
        print(f"Issue chains: {self.stats['issue_chains']}")
        print("\nIssues by type:")
        for issue, count in self.stats['issues_simulated'].items():
            print(f"  - {issue}: {count}")
        print("=" * 60)

    def get_stats(self) -> Dict:
        """Get current statistics."""
        return self.stats.copy()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def get_issue_types() -> List[str]:
    """Get list of all available issue types."""
    return [t.value for t in IssueType]


def get_issue_categories() -> Dict[str, List[str]]:
    """Get issue types organized by category."""
    return {
        "Network Issues": [
            IssueType.DNS_FAILURE.value,
            IssueType.CONNECTION_TIMEOUT.value,
            IssueType.SSL_ERROR.value,
            IssueType.PACKET_LOSS.value,
            IssueType.BANDWIDTH_THROTTLING.value,
            IssueType.PROXY_ERROR.value,
            IssueType.VPN_ISSUES.value,
            IssueType.WIFI_PROBLEMS.value,
        ],
        "System Issues": [
            IssueType.SLOW_COMPUTER.value,
            IssueType.HIGH_CPU.value,
            IssueType.MEMORY_LEAK.value,
            IssueType.DISK_FULL.value,
            IssueType.DRIVER_ISSUES.value,
            IssueType.BSOD.value,
            IssueType.BOOT_FAILURE.value,
        ],
        "Malware/Adware": [
            IssueType.ADWARE_INFECTION.value,
            IssueType.BROWSER_HIJACK.value,
            IssueType.POPUP_ADS.value,
            IssueType.CRYPTOMINER.value,
            IssueType.RANSOMWARE.value,
            IssueType.TROJAN.value,
            IssueType.SPYWARE.value,
        ],
        "Software Issues": [
            IssueType.APP_CRASH.value,
            IssueType.UPDATE_FAILURE.value,
            IssueType.PERMISSION_DENIED.value,
            IssueType.DLL_MISSING.value,
            IssueType.COMPATIBILITY.value,
        ],
    }


def get_issue_pattern(issue_type: str) -> Optional[IssuePattern]:
    """Get the pattern definition for an issue type."""
    try:
        return ISSUE_PATTERNS[IssueType(issue_type)]
    except (ValueError, KeyError):
        return None


# ============================================================================
# MAIN / DEMO
# ============================================================================

async def demo():
    """Demo the issue traffic generator."""
    print("\n" + "=" * 60)
    print("ISSUE TRAFFIC GENERATOR DEMO")
    print("=" * 60)

    # List available categories
    print("\nAvailable issue categories:")
    for category, issues in get_issue_categories().items():
        print(f"\n  {category}:")
        for issue in issues:
            pattern = get_issue_pattern(issue)
            if pattern:
                print(f"    - {issue}: {pattern.description}")

    # Run a short demo
    print("\n" + "-" * 60)
    print("Running 2-minute demo with random issues...")
    print("-" * 60)

    generator = IssueTrafficGenerator(
        issue_types=[
            IssueType.WIFI_PROBLEMS,
            IssueType.SLOW_COMPUTER,
            IssueType.ADWARE_INFECTION,
        ],
        frustration_mode=True,
        chaos_factor=0.3,
    )

    try:
        await generator.run(duration_minutes=2, issues_per_session=3)
    except KeyboardInterrupt:
        generator.stop()


if __name__ == "__main__":
    asyncio.run(demo())
