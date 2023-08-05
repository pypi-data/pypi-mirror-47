from MultiSC.MultiClient.EasyClient import EasyClient


def main():
    address = "195.154.243.51", 84
    user = EasyClient(address)
    user.connect()

    print(user.castom_request("printer", "name", name="hello"))
    print(user.castom_request("math", "sum", a=5, b=9))


main()
input("Enter to exit")
