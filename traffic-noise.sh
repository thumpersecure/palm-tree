#!/bin/bash
#
# traffic-noise.sh - Network Traffic Obfuscation Tool for Privacy Testing
# Generates randomized network traffic to obscure browsing patterns from trackers
# Designed for Kali Linux
#
# Usage: ./traffic-noise.sh [OPTIONS]
#   -n, --news-only       Browse random news sites only (default)
#   -v, --vps IP:PORT     Connect to specific VPS endpoint
#   -h, --headlines       Output news headlines fetched
#   -r, --randomize-id    Full identity randomization (MAC, DNS, timing)
#   -c, --chaos           Chaos mode - multi-bot simulation, erratic timing
#   -w, --workers NUM     Number of parallel workers (default: 1, max: 10)
#   -d, --duration MINS   Run for specified minutes (default: continuous)
#   -i, --interface IFACE Network interface for MAC spoofing (default: eth0)
#   -q, --quiet           Suppress most output
#   --help                Show this help message
#

set -e

# ============================================================================
# CONFIGURATION
# ============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default settings
MODE="news"
VPS_TARGET=""
SHOW_HEADLINES=false
RANDOMIZE_IDENTITY=false
DURATION=0  # 0 = continuous
INTERFACE="eth0"
QUIET=false
UDP_PORT_LOCAL=19999
CHAOS_MODE=false
PARALLEL_WORKERS=1

# Timing ranges (seconds)
MIN_DELAY=3
MAX_DELAY=45
MIN_SESSION=60
MAX_SESSION=300

# Chaos mode timing (more erratic)
CHAOS_MIN_DELAY=1
CHAOS_MAX_DELAY=120
BURST_MIN=3
BURST_MAX=15

# ============================================================================
# USER AGENTS - Diverse OS/Browser combinations
# ============================================================================

USER_AGENTS=(
    # Windows Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    # Windows Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
    # Windows Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    # macOS Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
    # macOS Chrome
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    # macOS Firefox
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.2; rv:121.0) Gecko/20100101 Firefox/121.0"
    # Linux Chrome
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    # Linux Firefox
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
    # iOS Safari
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"
    # Android Chrome
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36"
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36"
    # Older browsers (appear as different users)
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
    # Bots/Crawlers (intentional bot signatures)
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)"
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"
    "Twitterbot/1.0"
    # Unusual/Rare browsers
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Vivaldi/6.5"
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Brave/120"
    # Very old browsers
    "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)"
    # Exotic devices
    "Mozilla/5.0 (PlayStation; PlayStation 5/1.0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"
    "Mozilla/5.0 (Nintendo Switch; WifiWebAuthApplet) AppleWebKit/609.4 (KHTML, like Gecko) NF/6.0.2.21.3 NintendoBrowser/5.1.0.22474"
    "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36"
    "Mozilla/5.0 (SMART-TV; Linux; Tizen 6.5) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 Chrome/85.0.4183.93 TV Safari/537.36"
)

# ============================================================================
# BROWSER FINGERPRINT VARIATIONS
# ============================================================================

# Screen resolutions (for headers)
SCREEN_RESOLUTIONS=(
    "1920x1080" "2560x1440" "1366x768" "1536x864" "1440x900"
    "1280x720" "3840x2160" "2560x1080" "3440x1440" "1680x1050"
    "360x640" "375x667" "414x896" "390x844" "428x926"
)

# Timezones
TIMEZONES=(
    "America/New_York" "America/Los_Angeles" "America/Chicago" "America/Denver"
    "Europe/London" "Europe/Paris" "Europe/Berlin" "Europe/Moscow"
    "Asia/Tokyo" "Asia/Shanghai" "Asia/Singapore" "Australia/Sydney"
    "America/Sao_Paulo" "Africa/Cairo" "Asia/Dubai" "Pacific/Auckland"
)

# Accept headers variations
ACCEPT_HEADERS=(
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    "*/*"
)

# Encoding preferences
ACCEPT_ENCODINGS=(
    "gzip, deflate, br"
    "gzip, deflate"
    "gzip, deflate, br, zstd"
    "identity"
    "gzip"
)

# Connection types
CONNECTION_TYPES=(
    "keep-alive"
    "close"
    "keep-alive, Upgrade"
)

# Cache control headers (simulate different caching behaviors)
CACHE_CONTROLS=(
    "max-age=0"
    "no-cache"
    "no-store"
    ""
)

# Browsing patterns (simulate different user behaviors)
BROWSING_PATTERNS=(
    "normal"      # Regular intervals
    "bursty"      # Quick bursts then pause
    "slow"        # Very slow, careful browsing
    "erratic"     # Random timing
    "scanner"     # Fast, systematic (bot-like)
)

# ============================================================================
# DNS SERVERS - Well-known public DNS
# ============================================================================

DNS_SERVERS=(
    "8.8.8.8"           # Google Primary
    "8.8.4.4"           # Google Secondary
    "1.1.1.1"           # Cloudflare Primary
    "1.0.0.1"           # Cloudflare Secondary
    "9.9.9.9"           # Quad9 Primary
    "149.112.112.112"   # Quad9 Secondary
    "208.67.222.222"    # OpenDNS Primary
    "208.67.220.220"    # OpenDNS Secondary
    "64.6.64.6"         # Verisign Primary
    "64.6.65.6"         # Verisign Secondary
    "185.228.168.9"     # CleanBrowsing
    "76.76.19.19"       # Alternate DNS
    "94.140.14.14"      # AdGuard DNS
    "77.88.8.8"         # Yandex DNS
)

# ============================================================================
# NEWS SITES BY CATEGORY
# ============================================================================

# Lifestyle News
LIFESTYLE_NEWS=(
    "https://www.buzzfeed.com"
    "https://www.huffpost.com/life"
    "https://www.refinery29.com"
    "https://www.popsugar.com"
    "https://www.goodhousekeeping.com"
    "https://www.realsimple.com"
    "https://www.apartmenttherapy.com"
    "https://www.myrecipes.com"
    "https://www.allrecipes.com"
    "https://www.foodnetwork.com"
)

# World News
WORLD_NEWS=(
    "https://www.bbc.com/news/world"
    "https://www.reuters.com/world"
    "https://www.aljazeera.com"
    "https://www.theguardian.com/world"
    "https://apnews.com/world-news"
    "https://www.france24.com/en"
    "https://www.dw.com/en"
    "https://www.euronews.com"
    "https://www.npr.org/sections/world"
    "https://foreignpolicy.com"
)

# Technology News
TECH_NEWS=(
    "https://www.theverge.com"
    "https://techcrunch.com"
    "https://arstechnica.com"
    "https://www.wired.com"
    "https://www.cnet.com"
    "https://www.engadget.com"
    "https://www.zdnet.com"
    "https://www.tomshardware.com"
    "https://www.anandtech.com"
    "https://www.techmeme.com"
)

# Health News
HEALTH_NEWS=(
    "https://www.webmd.com"
    "https://www.healthline.com"
    "https://www.medicalnewstoday.com"
    "https://www.health.com"
    "https://www.everydayhealth.com"
    "https://www.prevention.com"
    "https://www.menshealth.com"
    "https://www.womenshealthmag.com"
    "https://www.self.com"
    "https://www.shape.com"
)

# Trending/General News
TRENDING_NEWS=(
    "https://news.google.com"
    "https://www.reddit.com/r/news"
    "https://www.reddit.com/r/worldnews"
    "https://news.ycombinator.com"
    "https://www.msn.com/en-us/news"
    "https://www.usatoday.com"
    "https://www.nbcnews.com"
    "https://www.cbsnews.com"
    "https://abcnews.go.com"
    "https://www.cnn.com"
)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

log_info() {
    if [ "$QUIET" = false ]; then
        echo -e "${GREEN}[INFO]${NC} $1"
    fi
}

log_warn() {
    if [ "$QUIET" = false ]; then
        echo -e "${YELLOW}[WARN]${NC} $1"
    fi
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_headline() {
    if [ "$SHOW_HEADLINES" = true ]; then
        echo -e "${CYAN}[HEADLINE]${NC} $1"
    fi
}

log_traffic() {
    if [ "$QUIET" = false ]; then
        echo -e "${BLUE}[TRAFFIC]${NC} $1"
    fi
}

# Generate random number in range
rand_range() {
    local min=$1
    local max=$2
    echo $(( RANDOM % (max - min + 1) + min ))
}

# Get random element from array
rand_element() {
    local arr=("$@")
    local idx=$(( RANDOM % ${#arr[@]} ))
    echo "${arr[$idx]}"
}

# Generate random MAC address (locally administered)
generate_mac() {
    printf '%02x:%02x:%02x:%02x:%02x:%02x\n' \
        $(( (RANDOM % 256) & 0xFE | 0x02 )) \
        $(( RANDOM % 256 )) \
        $(( RANDOM % 256 )) \
        $(( RANDOM % 256 )) \
        $(( RANDOM % 256 )) \
        $(( RANDOM % 256 ))
}

# Get random user agent
get_random_ua() {
    rand_element "${USER_AGENTS[@]}"
}

# Get random DNS server
get_random_dns() {
    rand_element "${DNS_SERVERS[@]}"
}

# Get random news URL from random category
get_random_news_url() {
    local category=$(rand_range 1 5)
    case $category in
        1) rand_element "${LIFESTYLE_NEWS[@]}" ;;
        2) rand_element "${WORLD_NEWS[@]}" ;;
        3) rand_element "${TECH_NEWS[@]}" ;;
        4) rand_element "${HEALTH_NEWS[@]}" ;;
        5) rand_element "${TRENDING_NEWS[@]}" ;;
    esac
}

# Get category name
get_category_name() {
    local category=$(rand_range 1 5)
    case $category in
        1) echo "Lifestyle" ;;
        2) echo "World" ;;
        3) echo "Technology" ;;
        4) echo "Health" ;;
        5) echo "Trending" ;;
    esac
}

# Get random browsing pattern
get_browsing_pattern() {
    rand_element "${BROWSING_PATTERNS[@]}"
}

# Get delay based on pattern
get_pattern_delay() {
    local pattern=$1
    case $pattern in
        "normal")
            rand_range 5 30
            ;;
        "bursty")
            # Either very fast or long pause
            if [ $(rand_range 1 10) -le 7 ]; then
                rand_range 1 3
            else
                rand_range 30 90
            fi
            ;;
        "slow")
            rand_range 45 180
            ;;
        "erratic")
            rand_range 1 120
            ;;
        "scanner")
            rand_range 1 5
            ;;
        *)
            rand_range $MIN_DELAY $MAX_DELAY
            ;;
    esac
}

# Generate random session ID (cookie-like)
generate_session_id() {
    cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 32 | head -n 1
}

# Generate random client hints
generate_client_hints() {
    local mobile=$(rand_range 0 1)
    local platform_idx=$(rand_range 0 4)
    local platforms=("Windows" "macOS" "Linux" "Android" "iOS")
    local platform="${platforms[$platform_idx]}"

    echo "Sec-CH-UA-Mobile: ?$mobile"
    echo "Sec-CH-UA-Platform: \"$platform\""
}

# Generate viewport dimensions
generate_viewport() {
    rand_element "${SCREEN_RESOLUTIONS[@]}"
}

# ============================================================================
# IDENTITY RANDOMIZATION FUNCTIONS
# ============================================================================

# Change MAC address (requires root)
change_mac_address() {
    local iface=$1
    local new_mac=$(generate_mac)

    if [ "$EUID" -ne 0 ]; then
        log_warn "MAC spoofing requires root privileges - skipping"
        return 1
    fi

    log_info "Changing MAC on $iface to $new_mac"

    # Try using macchanger first (common on Kali)
    if command -v macchanger &> /dev/null; then
        ip link set "$iface" down 2>/dev/null || true
        macchanger -m "$new_mac" "$iface" 2>/dev/null || true
        ip link set "$iface" up 2>/dev/null || true
    else
        # Fallback to ip command
        ip link set "$iface" down 2>/dev/null || true
        ip link set "$iface" address "$new_mac" 2>/dev/null || true
        ip link set "$iface" up 2>/dev/null || true
    fi

    return 0
}

# Set temporary DNS resolver
set_dns_resolver() {
    local dns_server=$1

    if [ "$EUID" -ne 0 ]; then
        log_warn "DNS change requires root privileges - using curl's --dns-servers instead"
        return 1
    fi

    log_info "Temporarily using DNS: $dns_server"

    # Backup and modify resolv.conf
    if [ ! -f /etc/resolv.conf.backup.trafficnoise ]; then
        cp /etc/resolv.conf /etc/resolv.conf.backup.trafficnoise 2>/dev/null || true
    fi

    echo "nameserver $dns_server" > /etc/resolv.conf 2>/dev/null || true
    return 0
}

# Restore original DNS
restore_dns() {
    if [ -f /etc/resolv.conf.backup.trafficnoise ]; then
        mv /etc/resolv.conf.backup.trafficnoise /etc/resolv.conf 2>/dev/null || true
        log_info "Restored original DNS configuration"
    fi
}

# ============================================================================
# TRAFFIC GENERATION FUNCTIONS
# ============================================================================

# Generate local UDP traffic
generate_local_udp() {
    local port=${1:-$UDP_PORT_LOCAL}
    local message="NOISE_$(date +%s)_$(rand_range 1000 9999)"

    log_traffic "Local UDP echo on port $port"

    # Send random UDP packets locally
    if command -v nc &> /dev/null; then
        echo "$message" | nc -u -w1 127.0.0.1 "$port" 2>/dev/null &
    elif command -v socat &> /dev/null; then
        echo "$message" | socat - UDP:127.0.0.1:"$port" 2>/dev/null &
    fi
}

# Fetch URL with randomized headers (maximum fingerprint variation)
fetch_url() {
    local url=$1
    local worker_id=${2:-0}
    local ua=$(get_random_ua)
    local dns=$(get_random_dns)

    # Random accept-language with many variations
    local langs=(
        "en-US,en;q=0.9"
        "en-GB,en;q=0.9"
        "en-US,en;q=0.9,es;q=0.8"
        "en-US,en;q=0.9,fr;q=0.8"
        "en-US,en;q=0.9,de;q=0.8"
        "es-ES,es;q=0.9,en;q=0.8"
        "fr-FR,fr;q=0.9,en;q=0.8"
        "de-DE,de;q=0.9,en;q=0.8"
        "pt-BR,pt;q=0.9,en;q=0.8"
        "ja-JP,ja;q=0.9,en;q=0.8"
        "zh-CN,zh;q=0.9,en;q=0.8"
        "ru-RU,ru;q=0.9,en;q=0.8"
        "ar-SA,ar;q=0.9,en;q=0.8"
        "ko-KR,ko;q=0.9,en;q=0.8"
        "it-IT,it;q=0.9,en;q=0.8"
    )
    local lang=$(rand_element "${langs[@]}")

    # Random referers (including social media and direct)
    local referers=(
        "https://www.google.com/"
        "https://www.google.com/search?q=$(echo "$url" | md5sum | cut -c1-8)"
        "https://www.bing.com/"
        "https://duckduckgo.com/"
        "https://search.yahoo.com/"
        "https://www.facebook.com/"
        "https://twitter.com/"
        "https://t.co/"
        "https://www.reddit.com/"
        "https://news.ycombinator.com/"
        "https://www.linkedin.com/"
        ""  # Direct visit
        ""  # Direct visit (weighted)
        ""  # Direct visit (weighted)
    )
    local referer=$(rand_element "${referers[@]}")

    # Get varied fingerprint components
    local accept=$(rand_element "${ACCEPT_HEADERS[@]}")
    local encoding=$(rand_element "${ACCEPT_ENCODINGS[@]}")
    local connection=$(rand_element "${CONNECTION_TYPES[@]}")
    local cache=$(rand_element "${CACHE_CONTROLS[@]}")
    local viewport=$(generate_viewport)
    local session_id=$(generate_session_id)

    # Randomize DNT header (some users have it, some don't)
    local dnt_val=$(rand_range 0 2)  # 0, 1, or skip entirely

    log_traffic "[W$worker_id] Fetching: $url"
    [ "$QUIET" = false ] && log_info "  UA: ${ua:0:60}..."
    [ "$QUIET" = false ] && log_info "  Lang: $lang | Viewport: $viewport"

    local curl_opts=(
        -s
        -L
        --max-time 30
        --connect-timeout 10
        -A "$ua"
        -H "Accept: $accept"
        -H "Accept-Language: $lang"
        -H "Accept-Encoding: $encoding"
        -H "Connection: $connection"
    )

    # Add DNT header randomly
    if [ $dnt_val -lt 2 ]; then
        curl_opts+=(-H "DNT: $dnt_val")
    fi

    # Add cache control randomly
    if [ -n "$cache" ]; then
        curl_opts+=(-H "Cache-Control: $cache")
    fi

    # Add referer if not empty
    if [ -n "$referer" ]; then
        curl_opts+=(-H "Referer: $referer")
    fi

    # Sometimes add Upgrade-Insecure-Requests
    if [ $(rand_range 0 1) -eq 1 ]; then
        curl_opts+=(-H "Upgrade-Insecure-Requests: 1")
    fi

    # Add Sec-CH-UA headers randomly (modern browsers)
    if [ $(rand_range 0 1) -eq 1 ]; then
        local mobile=$(rand_range 0 1)
        local platforms=("Windows" "macOS" "Linux" "Android" "iOS")
        local platform=$(rand_element "${platforms[@]}")
        curl_opts+=(-H "Sec-CH-UA-Mobile: ?$mobile")
        curl_opts+=(-H "Sec-CH-UA-Platform: \"$platform\"")
    fi

    # Add X-Requested-With for some requests (AJAX simulation)
    if [ $(rand_range 0 4) -eq 0 ]; then
        curl_opts+=(-H "X-Requested-With: XMLHttpRequest")
    fi

    # Randomize cookies (fake session tracking)
    if [ $(rand_range 0 2) -gt 0 ]; then
        local fake_cookies="_ga=GA1.2.${RANDOM}${RANDOM}.$(date +%s); _gid=GA1.2.${RANDOM}.$(date +%s); session=$session_id"
        curl_opts+=(-H "Cookie: $fake_cookies")
    fi

    # Try to use specific DNS if curl supports it
    if curl --help 2>&1 | grep -q "\-\-dns-servers"; then
        curl_opts+=(--dns-servers "$dns")
    fi

    # Randomize TCP settings via curl options
    if [ $(rand_range 0 1) -eq 1 ]; then
        curl_opts+=(--tcp-fastopen)
    fi

    local response
    response=$(curl "${curl_opts[@]}" "$url" 2>/dev/null)

    echo "$response"
}

# Extract and display headlines from HTML
extract_headlines() {
    local html=$1
    local url=$2

    if [ "$SHOW_HEADLINES" = false ]; then
        return
    fi

    # Extract potential headlines from common patterns
    local headlines
    headlines=$(echo "$html" | grep -oP '(?<=<h[123][^>]*>)[^<]+(?=</h[123]>)' 2>/dev/null | head -5)

    if [ -z "$headlines" ]; then
        # Try title tags
        headlines=$(echo "$html" | grep -oP '(?<=<title>)[^<]+(?=</title>)' 2>/dev/null | head -1)
    fi

    if [ -n "$headlines" ]; then
        echo -e "${CYAN}--- Headlines from $url ---${NC}"
        echo "$headlines" | while read -r line; do
            if [ -n "$line" ]; then
                # Clean up the headline
                line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | head -c 100)
                log_headline "$line"
            fi
        done
        echo ""
    fi
}

# Connect to VPS
connect_to_vps() {
    local target=$1
    local ip=$(echo "$target" | cut -d: -f1)
    local port=$(echo "$target" | cut -d: -f2)
    local ua=$(get_random_ua)

    log_traffic "Connecting to VPS: $ip:$port"

    # Try HTTPS first, then HTTP, then raw TCP
    local response
    response=$(curl -s -L --max-time 30 -A "$ua" "https://$ip:$port" 2>/dev/null) || \
    response=$(curl -s -L --max-time 30 -A "$ua" "http://$ip:$port" 2>/dev/null) || \
    response=$(echo "PING_$(date +%s)" | nc -w5 "$ip" "$port" 2>/dev/null) || true

    if [ -n "$response" ]; then
        log_info "VPS response received (${#response} bytes)"
    fi
}

# ============================================================================
# PARALLEL WORKER FUNCTIONS (Multi-bot simulation)
# ============================================================================

# Worker process - runs independently with its own identity
run_worker() {
    local worker_id=$1
    local pattern=$(get_browsing_pattern)
    local worker_ua=$(get_random_ua)

    log_info "[Worker $worker_id] Started with pattern: $pattern"
    log_info "[Worker $worker_id] Identity: ${worker_ua:0:40}..."

    local request_count=0
    local burst_count=0
    local in_burst=false

    while true; do
        # Check if we should stop
        if [ -f "/tmp/traffic_noise_stop_$$" ]; then
            log_info "[Worker $worker_id] Stopping..."
            break
        fi

        # Generate some local UDP noise
        if [ $(rand_range 0 4) -eq 0 ]; then
            generate_local_udp $((UDP_PORT_LOCAL + worker_id))
        fi

        # Fetch content
        if [ "$MODE" = "vps" ] && [ -n "$VPS_TARGET" ]; then
            connect_to_vps "$VPS_TARGET"
        else
            local url=$(get_random_news_url)
            local html
            html=$(fetch_url "$url" "$worker_id")

            if [ -n "$html" ] && [ "$SHOW_HEADLINES" = true ]; then
                extract_headlines "$html" "$url"
            fi
        fi

        request_count=$((request_count + 1))

        # Get delay based on pattern
        local delay
        if [ "$CHAOS_MODE" = true ]; then
            # Chaos mode: completely random and erratic
            delay=$(rand_range $CHAOS_MIN_DELAY $CHAOS_MAX_DELAY)

            # Occasionally change identity mid-session
            if [ $(rand_range 0 10) -eq 0 ] && [ "$RANDOMIZE_IDENTITY" = true ]; then
                log_info "[Worker $worker_id] Rotating identity..."
                change_mac_address "$INTERFACE" 2>/dev/null || true
            fi
        else
            delay=$(get_pattern_delay "$pattern")
        fi

        # Handle burst pattern
        if [ "$pattern" = "bursty" ]; then
            if [ "$in_burst" = true ]; then
                burst_count=$((burst_count + 1))
                if [ $burst_count -ge $(rand_range $BURST_MIN $BURST_MAX) ]; then
                    in_burst=false
                    burst_count=0
                    delay=$(rand_range 60 180)  # Long pause after burst
                    log_info "[Worker $worker_id] Burst complete, pausing ${delay}s"
                fi
            else
                if [ $(rand_range 0 5) -eq 0 ]; then
                    in_burst=true
                    delay=1
                    log_info "[Worker $worker_id] Starting burst..."
                fi
            fi
        fi

        # Occasionally change browsing pattern (simulate user behavior change)
        if [ $(rand_range 0 20) -eq 0 ]; then
            pattern=$(get_browsing_pattern)
            log_info "[Worker $worker_id] Switched to pattern: $pattern"
        fi

        sleep "$delay"
    done
}

# Spawn multiple workers
spawn_workers() {
    local num_workers=$1
    local pids=()

    log_info "Spawning $num_workers parallel workers..."

    for ((i=1; i<=num_workers; i++)); do
        run_worker "$i" &
        pids+=($!)
        sleep $(rand_range 1 5)  # Stagger worker starts
    done

    echo "${pids[@]}"
}

# ============================================================================
# MAIN SESSION LOOP
# ============================================================================

run_session() {
    local session_duration=$(rand_range $MIN_SESSION $MAX_SESSION)
    local session_end=$((SECONDS + session_duration))
    local request_count=0
    local pattern=$(get_browsing_pattern)

    log_info "Starting new session (duration: ${session_duration}s, pattern: $pattern)"

    # Randomize identity at session start if enabled
    if [ "$RANDOMIZE_IDENTITY" = true ]; then
        change_mac_address "$INTERFACE"
        set_dns_resolver "$(get_random_dns)"
    fi

    while [ $SECONDS -lt $session_end ]; do
        # Check duration limit
        if [ $DURATION -gt 0 ] && [ $SECONDS -ge $((DURATION * 60)) ]; then
            log_info "Duration limit reached"
            return 1
        fi

        # Generate local UDP noise periodically
        if [ $(( request_count % 3 )) -eq 0 ]; then
            generate_local_udp
        fi

        # Main traffic generation
        if [ "$MODE" = "vps" ] && [ -n "$VPS_TARGET" ]; then
            connect_to_vps "$VPS_TARGET"
        else
            local url=$(get_random_news_url)
            local category=$(get_category_name)
            log_info "Category: $category"

            local html
            html=$(fetch_url "$url" "0")

            if [ -n "$html" ]; then
                extract_headlines "$html" "$url"
            fi
        fi

        request_count=$((request_count + 1))

        # Random delay based on pattern
        local delay
        if [ "$CHAOS_MODE" = true ]; then
            delay=$(rand_range $CHAOS_MIN_DELAY $CHAOS_MAX_DELAY)
        else
            delay=$(get_pattern_delay "$pattern")
        fi

        log_info "Waiting ${delay}s before next request..."
        sleep "$delay"

        # Occasionally rotate identity in chaos mode
        if [ "$CHAOS_MODE" = true ] && [ "$RANDOMIZE_IDENTITY" = true ]; then
            if [ $(rand_range 0 5) -eq 0 ]; then
                log_info "Rotating identity mid-session..."
                change_mac_address "$INTERFACE"
            fi
        fi
    done

    return 0
}

# ============================================================================
# CLEANUP
# ============================================================================

cleanup() {
    log_info "Shutting down..."

    # Signal workers to stop
    touch "/tmp/traffic_noise_stop_$$"

    # Restore DNS if we changed it
    if [ "$RANDOMIZE_IDENTITY" = true ]; then
        restore_dns
    fi

    # Kill any background processes
    jobs -p | xargs -r kill 2>/dev/null || true

    # Cleanup stop file
    rm -f "/tmp/traffic_noise_stop_$$"

    log_info "Cleanup complete"
    exit 0
}

# ============================================================================
# HELP
# ============================================================================

show_help() {
    cat << 'EOF'
Traffic Noise Generator - Network Obfuscation Tool for Privacy Testing
=======================================================================

This tool generates randomized network traffic to help obscure your
browsing patterns from advertisers and data collectors. It can simulate
multiple "users" or "bots" to make real traffic patterns undetectable.

USAGE:
    ./traffic-noise.sh [OPTIONS]

OPTIONS:
    -n, --news-only         Browse random news sites only (default mode)
    -v, --vps IP:PORT       Connect to specific VPS endpoint instead of news
    -h, --headlines         Output news headlines fetched from sites
    -r, --randomize-id      Full identity randomization (MAC, DNS, timing)
                            Requires root privileges for MAC/DNS changes
    -c, --chaos             CHAOS MODE - Makes you appear as multiple bots!
                            Erratic timing, frequent identity rotation,
                            varied fingerprints, unpredictable patterns
    -w, --workers NUM       Number of parallel workers/identities (1-10)
                            Each worker has unique fingerprint & pattern
    -d, --duration MINS     Run for specified minutes (default: continuous)
    -i, --interface IFACE   Network interface for MAC spoofing (default: eth0)
    -q, --quiet             Suppress most output (errors still shown)
    --help                  Show this help message

EXAMPLES:
    # Basic news browsing with headlines
    ./traffic-noise.sh -n -h

    # RECOMMENDED: Full chaos mode (appear as multiple bots)
    sudo ./traffic-noise.sh -c -r -w 5 -h

    # Maximum obfuscation: 10 workers, chaos mode, identity rotation
    sudo ./traffic-noise.sh -c -r -w 10 -d 60

    # Full randomization with headlines for 30 minutes
    sudo ./traffic-noise.sh -r -h -d 30

    # Connect to VPS at 192.168.1.100:8080
    ./traffic-noise.sh -v 192.168.1.100:8080

    # Quiet mode for background operation
    ./traffic-noise.sh -n -q -d 60 &

NEWS CATEGORIES:
    - Lifestyle (recipes, home, entertainment)
    - World News (BBC, Reuters, AP, etc.)
    - Technology (Verge, TechCrunch, Wired, etc.)
    - Health (WebMD, Healthline, etc.)
    - Trending (Google News, Reddit, etc.)

BROWSING PATTERNS (automatically rotated):
    - normal:   Regular intervals (5-30s)
    - bursty:   Quick bursts then long pauses
    - slow:     Very slow browsing (45-180s)
    - erratic:  Completely random timing
    - scanner:  Fast, systematic (bot-like)

FEATURES:
    1. Randomized session timing (pattern-based)
    2. 30+ rotating user agents (browsers, bots, exotic devices)
    3. Random MAC address spoofing (requires root + macchanger)
    4. DNS server rotation (14 public DNS providers)
    5. OS fingerprint spoofing via user agent strings
    6. Multi-category news site rotation (50+ sites)
    7. Local UDP traffic generation for additional noise
    8. VPS connection mode for custom endpoints
    9. Headline extraction and display
    10. CHAOS MODE - Multi-bot simulation with erratic behavior

CHAOS MODE DETAILS (-c flag):
    Chaos mode makes your traffic appear as if multiple different
    users/bots are on your network simultaneously:
    - Completely erratic timing (1-120 seconds)
    - Frequent mid-session identity rotation
    - Mixed bot and human user agents
    - Varied browser fingerprints per request
    - Different browsing patterns running in parallel
    - Simulates traffic from different OS, devices, locations

REQUIREMENTS:
    - curl (required)
    - nc/netcat (optional, for UDP and VPS)
    - macchanger (optional, for MAC spoofing)
    - root privileges (optional, for MAC/DNS changes)

NOTES:
    - Press Ctrl+C to stop gracefully
    - MAC spoofing may temporarily disconnect network
    - Some sites may block automated requests
    - Use responsibly and in accordance with applicable laws
    - Best run with: sudo ./traffic-noise.sh -c -r -w 5

EOF
}

# ============================================================================
# ARGUMENT PARSING
# ============================================================================

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -n|--news-only)
                MODE="news"
                shift
                ;;
            -v|--vps)
                MODE="vps"
                VPS_TARGET="$2"
                shift 2
                ;;
            -h|--headlines)
                SHOW_HEADLINES=true
                shift
                ;;
            -r|--randomize-id)
                RANDOMIZE_IDENTITY=true
                shift
                ;;
            -c|--chaos)
                CHAOS_MODE=true
                shift
                ;;
            -w|--workers)
                PARALLEL_WORKERS="$2"
                # Validate workers count
                if ! [[ "$PARALLEL_WORKERS" =~ ^[0-9]+$ ]] || [ "$PARALLEL_WORKERS" -lt 1 ]; then
                    PARALLEL_WORKERS=1
                elif [ "$PARALLEL_WORKERS" -gt 10 ]; then
                    log_warn "Limiting workers to 10 (requested: $PARALLEL_WORKERS)"
                    PARALLEL_WORKERS=10
                fi
                shift 2
                ;;
            -d|--duration)
                DURATION="$2"
                shift 2
                ;;
            -i|--interface)
                INTERFACE="$2"
                shift 2
                ;;
            -q|--quiet)
                QUIET=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
}

# ============================================================================
# DEPENDENCY CHECK
# ============================================================================

check_dependencies() {
    local missing=()

    if ! command -v curl &> /dev/null; then
        missing+=("curl")
    fi

    if [ ${#missing[@]} -gt 0 ]; then
        log_error "Missing required dependencies: ${missing[*]}"
        log_error "Install with: apt install ${missing[*]}"
        exit 1
    fi

    # Optional dependencies warnings
    if ! command -v nc &> /dev/null && ! command -v netcat &> /dev/null; then
        log_warn "netcat not found - local UDP traffic disabled"
    fi

    if [ "$RANDOMIZE_IDENTITY" = true ]; then
        if ! command -v macchanger &> /dev/null; then
            log_warn "macchanger not found - using ip command for MAC changes"
        fi
        if [ "$EUID" -ne 0 ]; then
            log_warn "Not running as root - MAC/DNS spoofing will be limited"
        fi
    fi
}

# ============================================================================
# BANNER
# ============================================================================

show_banner() {
    if [ "$QUIET" = true ]; then
        return
    fi

    cat << 'EOF'
  _____            __  __ _        _   _       _
 |_   _| __ __ _ / _|/ _(_) ___  | \ | | ___ (_)___  ___
   | || '__/ _` | |_| |_| |/ __| |  \| |/ _ \| / __|/ _ \
   | || | | (_| |  _|  _| | (__  | |\  | (_) | \__ \  __/
   |_||_|  \__,_|_| |_| |_|\___| |_| \_|\___/|_|___/\___|

  Network Traffic Obfuscation Tool - Privacy Testing
EOF
    echo ""
    echo "  Mode: $MODE"
    [ -n "$VPS_TARGET" ] && echo "  VPS Target: $VPS_TARGET"
    echo "  Headlines: $SHOW_HEADLINES"
    echo "  Identity Randomization: $RANDOMIZE_IDENTITY"
    echo "  Chaos Mode: $CHAOS_MODE"
    echo "  Parallel Workers: $PARALLEL_WORKERS"
    [ $DURATION -gt 0 ] && echo "  Duration: ${DURATION} minutes" || echo "  Duration: Continuous"
    echo "  Interface: $INTERFACE"
    echo ""
    if [ "$CHAOS_MODE" = true ]; then
        echo -e "  ${YELLOW}CHAOS MODE ACTIVE - Simulating multiple bots${NC}"
    fi
    echo "  Press Ctrl+C to stop"
    echo "=============================================="
    echo ""
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    parse_args "$@"
    check_dependencies

    # Set up signal handlers
    trap cleanup SIGINT SIGTERM

    show_banner

    log_info "Starting traffic generation..."

    # Remove any stale stop file
    rm -f "/tmp/traffic_noise_stop_$$"

    # Start local UDP listeners in background (for echo testing)
    if command -v nc &> /dev/null; then
        for ((p=0; p<PARALLEL_WORKERS; p++)); do
            local port=$((UDP_PORT_LOCAL + p))
            (while true; do nc -lu -p $port 2>/dev/null || sleep 1; done) &
        done
        log_info "Local UDP listeners started on ports $UDP_PORT_LOCAL-$((UDP_PORT_LOCAL + PARALLEL_WORKERS - 1))"
    fi

    # Check if using parallel workers
    if [ "$PARALLEL_WORKERS" -gt 1 ]; then
        log_info "Starting $PARALLEL_WORKERS parallel workers (multi-bot simulation)..."

        # Spawn workers
        local worker_pids
        worker_pids=$(spawn_workers "$PARALLEL_WORKERS")

        # Wait for duration or interrupt
        if [ "$DURATION" -gt 0 ]; then
            log_info "Running for $DURATION minutes..."
            sleep $((DURATION * 60))
            log_info "Duration reached, stopping workers..."
            touch "/tmp/traffic_noise_stop_$$"
            sleep 5
        else
            # Wait indefinitely
            log_info "Running continuously. Press Ctrl+C to stop."
            wait
        fi
    else
        # Single worker mode (original behavior)
        while true; do
            if ! run_session; then
                break
            fi

            log_info "Session complete, starting new session..."

            # Brief pause between sessions
            sleep $(rand_range 5 15)
        done
    fi

    cleanup
}

# Run main
main "$@"
