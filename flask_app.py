from flask import Flask, render_template, request, jsonify
from tinydb import TinyDB, Query
import pandas as pd

app = Flask(_name_)

db = TinyDB('crypto_data.json')

crypto_data = [
    {"Symbol": "AAVE", "Name": "Aave", "Founders": "Stani Kulechov", "Founded": 2017, "Uses Smart Contracts": "Yes", "Blockchain Use": "Decentralized lending and borrowing on Ethereum", "Main Project Idea": "Decentralized finance protocols", "Famous Smart Contract": "Aave Lending Protocol"},
    {"Symbol": "ADA", "Name": "Cardano", "Founders": "Charles Hoskinson", "Founded": 2017, "Uses Smart Contracts": "Yes", "Blockchain Use": "Proof-of-stake blockchain for dApps", "Main Project Idea": "Scalable blockchain for smart contracts and dApps", "Famous Smart Contract": "Marlowe (financial contracts)"},
    {"Symbol": "ALGO", "Name": "Algorand", "Founders": "Silvio Micali", "Founded": 2019, "Uses Smart Contracts": "Yes", "Blockchain Use": "Pure proof-of-stake protocol", "Main Project Idea": "Speed and efficiency in transactions", "Famous Smart Contract": "Algorand Standard Assets"},
    {"Symbol": "AVAX", "Name": "Avalanche", "Founders": "Emin Gün Sirer", "Founded": 2020, "Uses Smart Contracts": "Yes", "Blockchain Use": "Unique consensus mechanism", "Main Project Idea": "Highly scalable blockchain platform", "Famous Smart Contract": "Pangolin Exchange"},
    {"Symbol": "BAT", "Name": "Basic Attention Token", "Founders": "Brendan Eich", "Founded": 2017, "Uses Smart Contracts": "Yes", "Blockchain Use": "Ad revenue distribution on Ethereum", "Main Project Idea": "Change digital advertising dynamics", "Famous Smart Contract": "Brave Rewards"},
    {"Symbol": "BCH", "Name": "Bitcoin Cash", "Founders": "Fork by Roger Ver", "Founded": 2017, "Uses Smart Contracts": "No", "Blockchain Use": "Increased block size for scalability", "Main Project Idea": "Faster, cheaper transactions", "Famous Smart Contract": ""},
    {"Symbol": "BNB", "Name": "Binance Coin", "Founders": "Changpeng Zhao (CZ)", "Founded": 2017, "Uses Smart Contracts": "Yes", "Blockchain Use": "Utility and transaction fees on Binance platforms", "Main Project Idea": "Utility token for Binance exchange", "Famous Smart Contract": "PancakeSwap (on Binance Smart Chain)"},
    {"Symbol": "BTC", "Name": "Bitcoin", "Founders": "Satoshi Nakamoto", "Founded": 2009, "Uses Smart Contracts": "No", "Blockchain Use": "Proof-of-work blockchain", "Main Project Idea": "Digital currency and store of value", "Famous Smart Contract": ""},
    {"Symbol": "DASH", "Name": "Dash", "Founders": "Evan Duffield", "Founded": 2014, "Uses Smart Contracts": "No", "Blockchain Use": "Privacy-focused digital cash", "Main Project Idea": "Instant and private transactions", "Famous Smart Contract": ""},
    {"Symbol": "DCR", "Name": "Decred", "Founders": "Project by Company 0", "Founded": 2016, "Uses Smart Contracts": "Yes", "Blockchain Use": "Governance-focused blockchain", "Main Project Idea": "Community governance of blockchain operations", "Famous Smart Contract": "Politeia"},
    {"Symbol": "DOGE", "Name": "Dogecoin", "Founders": "Billy Markus, Jackson Palmer", "Founded": 2013, "Uses Smart Contracts": "No", "Blockchain Use": "Cryptocurrency for tipping and donations", "Main Project Idea": "Fun and community-driven digital currency", "Famous Smart Contract": ""},
    {"Symbol": "ENJ", "Name": "Enjin Coin", "Founders": "Maxim Blagov, Witek Radomski", "Founded": 2017, "Uses Smart Contracts": "Yes", "Blockchain Use": "Token for virtual goods on Ethereum", "Main Project Idea": "Create and manage virtual goods", "Famous Smart Contract": "Enjin Platform"},
    {"Symbol": "EOS", "Name": "EOS.IO", "Founders": "Dan Larimer, Brendan Blumer", "Founded": 2018, "Uses Smart Contracts": "Yes", "Blockchain Use": "Scalable blockchain for dApps", "Main Project Idea": "Decentralized applications on a scalable blockchain", "Famous Smart Contract": "Everipedia"},
    {"Symbol": "ETC", "Name": "Ethereum Classic", "Founders": "Original Ethereum Community", "Founded": 2016, "Uses Smart Contracts": "Yes", "Blockchain Use": "Continuation of original Ethereum blockchain", "Main Project Idea": "Keep the original Ethereum going", "Famous Smart Contract": ""},
    {"Symbol": "ETH", "Name": "Ethereum", "Founders": "Vitalik Buterin", "Founded": 2015, "Uses Smart Contracts": "Yes", "Blockchain Use": "Platform for decentralized applications (dApps)", "Main Project Idea": "Smart contract and dApp development", "Famous Smart Contract": "Uniswap"},
    {"Symbol": "FIL", "Name": "Filecoin", "Founders": "Juan Benet", "Founded": 2017, "Uses Smart Contracts": "Yes", "Blockchain Use": "Decentralized storage network", "Main Project Idea": "Decentralized data storage marketplace", "Famous Smart Contract": ""},
    {"Symbol": "HBAR", "Name": "Hedera Hashgraph", "Founders": "Leemon Baird", "Founded": 2018, "Uses Smart Contracts": "Yes", "Blockchain Use": "Hashgraph for fast, secure applications", "Main Project Idea": "Fast, fair, and secure decentralized applications", "Famous Smart Contract": ""},
    {"Symbol": "HT", "Name": "Huobi Token", "Founders": "Leon Li", "Founded": 2018, "Uses Smart Contracts": "Yes", "Blockchain Use": "Utility token for Huobi crypto exchange", "Main Project Idea": "Reduce exchange fees and enable voting on exchange decisions", "Famous Smart Contract": ""},
    {"Symbol": "KLAY", "Name": "Klaytn", "Founders": "Jaesun Han", "Founded": 2019, "Uses Smart Contracts": "Yes", "Blockchain Use": "Public blockchain platform", "Main Project Idea": "User-friendly blockchain experience", "Famous Smart Contract": "Klaytn Swap"},
    {"Symbol": "KSM", "Name": "Kusama", "Founders": "Gavin Wood", "Founded": 2019, "Uses Smart Contracts": "Yes", "Blockchain Use": "Canary network for Polkadot", "Main Project Idea": "Early deployment and testing for Polkadot projects", "Famous Smart Contract": "Karura Swap"},
    {"Symbol": "LINK", "Name": "Chainlink", "Founders": "Sergey Nazarov", "Founded": 2017, "Uses Smart Contracts": "Yes", "Blockchain Use": "Oracle network for secure data feeds", "Main Project Idea": "Link smart contracts with real-world data", "Famous Smart Contract": ""},
    {"Symbol": "LTC", "Name": "Litecoin", "Founders": "Charlie Lee", "Founded": 2011, "Uses Smart Contracts": "No", "Blockchain Use": "Lighter, faster version of Bitcoin", "Main Project Idea": "Improved transaction speeds and efficiencies", "Famous Smart Contract": ""},
    {"Symbol": "MANA", "Name": "Decentraland", "Founders": "Ariel Meilich, Esteban Ordano", "Founded": 2017, "Uses Smart Contracts": "Yes", "Blockchain Use": "Virtual reality platform on Ethereum", "Main Project Idea": "Virtual reality platform powered by Ethereum", "Famous Smart Contract": "Decentraland Marketplace"},
    {"Symbol": "MATIC", "Name": "Polygon", "Founders": "Jaynti Kanani, Sandeep Nailwal, Anurag Arjun", "Founded": 2017, "Uses Smart Contracts": "Yes", "Blockchain Use": "Ethereum scaling and infrastructure development", "Main Project Idea": "Scalable and instant blockchain transactions", "Famous Smart Contract": "QuickSwap"},
    {"Symbol": "MKR", "Name": "Maker", "Founders": "Rune Christensen", "Founded": 2017, "Uses Smart Contracts": "Yes", "Blockchain Use": "Decentralized autonomous organization on Ethereum", "Main Project Idea": "Minimize the volatility of its own stablecoin DAI", "Famous Smart Contract": "MakerDAO"},
    {"Symbol": "NEO", "Name": "NEO", "Founders": "Da Hongfei, Erik Zhang", "Founded": 2014, "Uses Smart Contracts": "Yes", "Blockchain Use": "Platform for a smart economy", "Main Project Idea": "Digital assets and identities with smart contracts", "Famous Smart Contract": "NeoLine Wallet"},
    {"Symbol": "QTUM", "Name": "Qtum", "Founders": "Patrick Dai", "Founded": 2016, "Uses Smart Contracts": "Yes", "Blockchain Use": "Merge of Bitcoin and Ethereum technologies", "Main Project Idea": "Build decentralized applications more securely", "Famous Smart Contract": ""},
    {"Symbol": "SNX", "Name": "Synthetix", "Founders": "Kain Warwick", "Founded": 2018, "Uses Smart Contracts": "Yes", "Blockchain Use": "Derivatives trading on Ethereum", "Main Project Idea": "Access to a variety of assets without owning them", "Famous Smart Contract": "Synthetix Exchange"},
    {"Symbol": "THETA", "Name": "Theta Network", "Founders": "Mitch Liu, Jieyi Long", "Founded": 2017, "Uses Smart Contracts": "Yes", "Blockchain Use": "Video streaming network", "Main Project Idea": "Decentralized video streaming", "Famous Smart Contract": "Theta.tv"},
    {"Symbol": "TRX", "Name": "TRON", "Founders": "Justin Sun", "Founded": 2017, "Uses Smart Contracts": "Yes", "Blockchain Use": "Entertainment and content sharing platform", "Main Project Idea": "Decentralized internet and its infrastructure", "Famous Smart Contract": "JUSTSwap"},
    {"Symbol": "USDC", "Name": "USD Coin", "Founders": "Circle and Coinbase", "Founded": 2018, "Uses Smart Contracts": "Yes", "Blockchain Use": "Stablecoin tied to USD", "Main Project Idea": "Stable digital dollar currency", "Famous Smart Contract": ""},
    {"Symbol": "USDT", "Name": "Tether", "Founders": "Brock Pierce, Reeve Collins, Craig Sellars", "Founded": 2014, "Uses Smart Contracts": "Yes", "Blockchain Use": "Stablecoin tied to USD", "Main Project Idea": "Stable digital dollar currency", "Famous Smart Contract": ""},
    {"Symbol": "VET", "Name": "VeChain", "Founders": "Sunny Lu", "Founded": 2015, "Uses Smart Contracts": "Yes", "Blockchain Use": "Supply chain management and business processes", "Main Project Idea": "Enhance supply chain protocols and processes", "Famous Smart Contract": "VeChain ToolChain"},
    {"Symbol": "WAVES", "Name": "Waves", "Founders": "Alexander Ivanov", "Founded": 2016, "Uses Smart Contracts": "Yes", "Blockchain Use": "Custom blockchain tokens system", "Main Project Idea": "Enable creation of custom tokens", "Famous Smart Contract": "Neutrino USD (USDN)"},
    {"Symbol": "XEM", "Name": "NEM", "Founders": "UtopianFuture (pseudonym)", "Founded": 2015, "Uses Smart Contracts": "Yes", "Blockchain Use": "Smart asset system", "Main Project Idea": "Create a more secure and streamlined economy", "Famous Smart Contract": ""},
    {"Symbol": "XLM", "Name": "Stellar", "Founders": "Jed McCaleb", "Founded": 2014, "Uses Smart Contracts": "Yes", "Blockchain Use": "Low-cost financial services to fight poverty", "Main Project Idea": "Improve low-cost international money transfers", "Famous Smart Contract": "Stellar Smart Contracts (SSC)"},
    {"Symbol": "XMR", "Name": "Monero", "Founders": "Nicolas van Saberhagen (pseudonym)", "Founded": 2014, "Uses Smart Contracts": "No", "Blockchain Use": "Privacy-focused cryptocurrency", "Main Project Idea": "Secure, private and untraceable currency", "Famous Smart Contract": ""},
    {"Symbol": "XRP", "Name": "XRP", "Founders": "Chris Larsen, Jed McCaleb", "Founded": 2012, "Uses Smart Contracts": "No", "Blockchain Use": "Digital payment protocol", "Main Project Idea": "Fast and efficient financial transactions", "Famous Smart Contract": ""},
    {"Symbol": "XTZ", "Name": "Tezos", "Founders": "Arthur Breitman", "Founded": 2018, "Uses Smart Contracts": "Yes", "Blockchain Use": "Self-amending cryptographic ledger", "Main Project Idea": "Smart contract safety and decentralized voting", "Famous Smart Contract": "Dexter"},
    {"Symbol": "YFI", "Name": "Yearn.finance", "Founders": "Andre Cronje", "Founded": 2020, "Uses Smart Contracts": "Yes", "Blockchain Use": "DeFi aggregator service", "Main Project Idea": "Maximize yield farming profits automatically", "Famous Smart Contract": "Yearn Vaults"},
    {"Symbol": "ZEC", "Name": "Zcash", "Founders": "Zooko Wilcox", "Founded": 2016, "Uses Smart Contracts": "Yes", "Blockchain Use": "Privacy-protecting digital currency", "Main Project Idea": "Enhance privacy for digital transactions", "Famous Smart Contract": ""},
    {"Symbol": "ZIL", "Name": "Zilliqa", "Founders": "Amrit Kumar, Xinshu Dong", "Founded": 2017, "Uses Smart Contracts": "Yes", "Blockchain Use": "High-throughput public blockchain", "Main Project Idea": "Scale blockchain technologies for wider application", "Famous Smart Contract": "Zilliqa Planet"}
    ]
db.insert_multiple(crypto_data)

df = pd.DataFrame(crypto_data, columns=["Symbol", "Name"])

@app.route('/')
def index():
    return render_template('index.html', df=df, ids = list(range(len(df))))


@app.route('/crypto')
def crypto():
    ticker = request.args.get("cryptocode")

    Crypto = Query()
    crypto_info = db.search(Crypto.Symbol == ticker)

    if crypto_info:
        return jsonify(crypto_info[0])
    else:
        return jsonify({"error": "Cryptocurrency not found for the given ticker"}), 404

if _name_ == '_main_':
    app.run(debug=True)

if _name_ == '_main_':
    app.run(debug=True)