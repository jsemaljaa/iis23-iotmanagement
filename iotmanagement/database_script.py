from db.models import Parameter

# Create parameters
temperature = Parameter.objects.create(name='Temperature', possible_values="N", value=0)
humidity = Parameter.objects.create(name='Humidity', possible_values="P", value=0)
