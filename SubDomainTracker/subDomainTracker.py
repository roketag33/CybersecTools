import dns.resolver

def load_subdomains(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def enumerate_subdomains(domain, subdomains):
    found_subdomains = []
    for subdomain in subdomains:
        try:
            target = f"{subdomain}.{domain}"
            answers = dns.resolver.resolve(target, 'A')
            found_subdomains.append(target)
            print(f"Found subdomain: {target}")
        except dns.resolver.NXDOMAIN:
            continue
        except Exception as e:
            print(f"Error resolving {target}: {e}")
    return found_subdomains

def main():
    domain = input("Enter the domain to scan: ")
    subdomains_list = load_subdomains("subdomains.txt")
    found = enumerate_subdomains(domain, subdomains_list)

    print("\nFound subdomains:")
    for subdomain in found:
        print(subdomain)

if __name__ == "__main__":
    main()
