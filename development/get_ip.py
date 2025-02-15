import boto3

# Tworzymy klienta EC2
ec2 = boto3.client('ec2', region_name='us-east-1')  # Zmień na swój region

# Podaj ID swojej instancji
instance_id = "i-xxxxxxxxxxxxxxxxx"

# Pobieramy informacje o instancji
response = ec2.describe_instances(InstanceIds=[instance_id])

# Odczytujemy publiczny IP
public_ip = response['Reservations'][0]['Instances'][0].get('PublicIpAddress')

if public_ip:
    print(f"Aktualny publiczny IP: {public_ip}")
else:
    print("Instancja nie ma przypisanego publicznego IP (może być zatrzymana).")
