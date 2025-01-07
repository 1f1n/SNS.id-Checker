import requests

USDC_MINT = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'
SOL_MINT = 'So11111111111111111111111111111111111111112'

def getDomainPrice(domainName: str, maxPriceUSDC: float, maxPriceSOL: float):
    url = f"https://sns-api.bonfida.com/v2/domains/current-listing/{domainName.lower()}"
    headers = {"Content-Type": "application/json"}

    try:
        req = requests.get(url, headers=headers)
        
        if req.status_code == 200:
            try:
                response = req.json()
                if response is not None:

                    avail = response.get("availability_id", 0)
                    if avail == 0:
                        avail = False
                    else:
                        avail = True

                    price = response.get("price", None)
                    quoteMint = response.get("quote_mint", None)

                    if price is not None:
                        if quoteMint == USDC_MINT and price <= maxPriceUSDC:
                            return price, avail, 'USDC'
                        elif quoteMint == SOL_MINT and price <= maxPriceSOL:
                            return price, avail, 'SOL'
                        else:
                            return None, None, None
                    else:
                        return None, None, None
                else:
                    print(f"{domainName} is not a registered domain, register it here -> https://sns.id.")
                    with open('unregistered.txt', 'a') as av:
                        av.write(f"{domainName}\n")
                    return None, None, None
            except ValueError:
                print(f"{domainName} is not valid JSON.")
                return None, None, None
        else:
            print(f"{domainName} ratelimited. Status code: {req.status_code}")
            return None, None, None
    except requests.RequestException as e:
        print(f"Request failed for {domainName}. Error: {e}")
        return None, None, None

def main():
    maxPriceUSDC = float(input("Enter max price in USDC: "))
    maxPriceSOL = float(input("Enter max price in SOL: "))

    with open('domains.txt', 'r') as getNames:
        names = getNames.read().splitlines()

    for name in names:
        name = name.strip()
        price, avail, currency = getDomainPrice(name, maxPriceUSDC, maxPriceSOL)
        if price is not None and avail:
            with open('available.txt', 'a') as av:
                av.write(f"{name} | {price} {currency}\n")
            print(f"{name}: {price} {currency} (Available: {avail})")

if __name__ == "__main__":
    main()
