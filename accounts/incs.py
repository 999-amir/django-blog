from accounts.models import CostumeUser


def check_signup_data(name, email, password_1, password_2):
    response = {
        'mode': False,
        'message': ''
    }
    if password_1 and password_2:
        if password_1 != password_2:
            response['message'] = 'passwords are not the same'
            return response
        elif len(password_1) < 8:
            response['message'] = 'password should be more than 8 charector'
            return response
        elif not any(i.isalpha() for i in password_1):
            response['message'] = 'password must have at least one alpha character'
            return response
        elif not any(i.isupper() for i in password_1):
            response['message'] = 'password must have at least one upper character'
            return response
        elif not any(i.isnumeric() for i in password_1):
            response['message'] = 'password must have at least one number'
            return response
        elif not any(i.islower() for i in password_1):
            response['message'] = 'password most have at least one slower character'
            return response
    else:
        response['message'] = 'passwords needed'
        return response
    if CostumeUser.objects.filter(email=email).exists():
        response['message'] = 'this email has been registered before'
        return response
    elif CostumeUser.objects.filter(name=name).exists():
        response['message'] = 'this name has been taken before'
        return response
    response['mode'] = True
    response['message'] = 'user created'
    return response


def check_password_strength(password_1, password_2):
    response = {
        'mode': False,
        'message': ''
    }
    if password_1 and password_2:
        if password_1 != password_2:
            response['message'] = 'passwords are not the same'
            return response
        elif len(password_1) < 8:
            response['message'] = 'password should be more than 8 charector'
            return response
        elif not any(i.isalpha() for i in password_1):
            response['message'] = 'password must have at least one alpha character'
            return response
        elif not any(i.isupper() for i in password_1):
            response['message'] = 'password must have at least one upper character'
            return response
        elif not any(i.isnumeric() for i in password_1):
            response['message'] = 'password must have at least one number'
            return response
        elif not any(i.islower() for i in password_1):
            response['message'] = 'password most have at least one slower character'
            return response
    else:
        response['message'] = 'passwords needed'
        return response
    response['mode'] = True
    response['message'] = 'passwords are correct'
    return response
