import requests

def pegaPLD(Data_Fwd):

    url = 'https://api-safira-on-prisma.safiraenergia.com.br/ccee-dessem-prices?start=2023-08-07T03:00:00.000Z'

    r = requests.get(url, verify=False)

    return r.text