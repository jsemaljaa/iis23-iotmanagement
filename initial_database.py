import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iotmanagement.settings")
django.setup()

from django.contrib.auth.models import User


from db.models import UserProfile, \
                        Parameter, \
                           Device, \
                           System, \
                     Notification, \
                       Invitation, \
                    SystemDevices, \
                      UserSystems, \
                  DeviceParameter  \



def create_user(username, email, password, name, surname, location, role):
    user = User.objects.create_user(username=username, email=email, password=password)
    user_profile = UserProfile.objects.create(
        user=user,
        name=name,
        surname=surname,
        location=location,
        email=email,
        role=role
    )
    return user_profile


def create_parameter(name, possible_values):
    return Parameter.objects.create(name=name, possible_values=possible_values)


def create_device(identifier, alias, created_by):
    return Device.objects.create(identifier=identifier, alias=alias, created_by=created_by)


def create_system(name, description, admin):
    return System.objects.create(
        name=name,
        description=description,
        number_of_devices=0,
        number_of_users=1,
        admin=admin
    )


def create_system_devices(system, device):
    system_device = SystemDevices.objects.create(system=system, device=device)

    system.number_of_devices += 1
    system.save()

    return system_device


def create_user_systems(user, system):
    return UserSystems.objects.create(user=user, system=system)


def create_device_parameter(device, parameter, value):
    return DeviceParameter.objects.create(device=device, parameter=parameter, value=value)


def populate_data():
    user_admin = create_user('admin', 'xlogin00@vutbr.cz', 'admin', 'Admin', 'Admin', 'Brno', 'admin')
    user_creator = create_user('creator', 'xlogin00@vutbr.cz', 'creator', 'Creator', 'Creator', 'Brno', 'creator')
    user_broker = create_user('broker', 'xlogin00@vutbr.cz', 'broker', 'Broker', 'Broker', 'Brno', 'broker')
    user_normal = create_user('user', 'xlogin00@vutbr.cz', 'user', 'User', 'User', 'Brno', 'user')

    temperature_parameter = create_parameter('Temperature', Parameter.PossibleValue.NUMERIC)
    humidity_parameter = create_parameter('Humidity', Parameter.PossibleValue.PERCENTAGE)
    brightness_parameter = create_parameter('Brightness', Parameter.PossibleValue.PERCENTAGE)

    sensor_device = create_device('Sensor', '', user_admin)
    lamp_device = create_device('Lamp', 'Alias', user_creator)

    system_1 = create_system('Admin Home', 'This is example home of an admin', user_admin)
    system_2 = create_system('User Home', 'This is example home of a user', user_creator)

    create_device_parameter(sensor_device, temperature_parameter, 23)
    create_device_parameter(sensor_device, humidity_parameter, 66)
    create_device_parameter(lamp_device, brightness_parameter, 79)

    create_system_devices(system_1, lamp_device)
    create_system_devices(system_2, sensor_device)
    create_system_devices(system_2, lamp_device)

    create_user_systems(user_admin, system_1)
    create_user_systems(user_creator, system_2)


if __name__ == "__main__":
    populate_data()
