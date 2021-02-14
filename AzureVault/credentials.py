from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Intialize credential
default_credential = DefaultAzureCredential()

# create a secret client
secret_client = SecretClient(
    # to be taken from azure portal
    vault_url="https://sarit-secret-key.vault.azure.net/",
    credential=default_credential
)

# get a secret
my_secret = secret_client.get_secret(
    name='saerit-vault-secret'  # generate from secret tab
)

print(my_secret.value)
